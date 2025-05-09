from django.shortcuts import render,redirect
from spoon_and_spice.db_connect import connect_db
from django.contrib import messages
from django.conf import settings


db=connect_db()
collection=db['user']
dishcollection=db['dishes']



# Create your views here.
def register(request):
  if request.method=='POST':
    name=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('password')

    excisting_user=collection.find_one({"email":email})
    if excisting_user:
      messages.error(request,"ALREADY REGISTERED! PLEASE LOGIN")
      return redirect('login')

    else:
      collection.insert_one({"name":name,"email":email,"password":password})
      user=collection.find_one({"email":email})
      if user:
        request.session['user_id']=str(user['_id'])
        return redirect('home')
      
    
    
  return render(request,"register.html")


def login(request):
  if request.method=="POST":
    email=request.POST.get("email")
    password=request.POST.get("password")


    user=collection.find_one({"email":email})
    if user:
      if password==user['password']:
        request.session['user_id']=str(user['_id'])
        return redirect('home')
      else:
        messages.error(request,"invalid credentials")
    else:
      messages.error(request,"please sign up!")
      return redirect('register')
        


  return render(request,"login.html")

def home(request):
    categories = list(dishcollection.distinct("category"))  # Get distinct categories
    cuisines = list(dishcollection.distinct("cuisine"))  # Get distinct cuisines
    general_categories = list(dishcollection.distinct("general"))  # Get distinct general categories
    
    return render(request, 'home.html', {
        'categories': categories,
        'cuisines': cuisines,
        'general_categories': general_categories,
    })

  

def add_recepie(request):
  if request.method=="POST":
    owner=request.POST.get('ownername')
    dish_name=request.POST.get('dish-name')
    owner_email=request.POST.get('owner_email')
    veg_non=request.POST.get('veg-nonveg')
    category=request.POST.get('category')
    no_of_people=request.POST.get('noofppl')
    dish_img=request.POST.get('dish-img')
    dish_video=request.POST.get('dish-vdo')
    procedure=request.POST.get('procedure')
    ingredients=request.POST.get('ingredients')
    dish_cate=request.POST.get('dish-cat')

    dishcollection.insert_many([{"dish_name":dish_name,"owner":owner,"owner_email":owner_email,"veg_nonveg":veg_non,"category":category,"no_people":no_of_people,"cusine":dish_cate,"ingredients":ingredients,"procedure":procedure,"dish_img":dish_img,"dish_video":dish_video}])

    return redirect('home')

  return render(request,"addrecipie.html")

def search_dish(request):
  dish = None
  error_message = None
    
  if request.method == 'POST':  
        query = request.POST.get('query')
        if query:
            
            dish = dishcollection.find_one({"dish_name": {'$regex': query, '$options': 'i'}})

            if not dish:
                error_message = "Dish not found."

  return render(request,"dish.html" ,{'dish': dish, 'error_message': error_message})



def category_dishes(request, category_name=None, cuisine_name=None, general_name=None):
    error_message = None
    dishes = []

    if category_name:
        # Find dishes based on category
        dishes = list(dishcollection.find({"category": {"$in": [category_name]}}))
        #print(f"Dishes found for category '{category_name}': {dishes}")

    if cuisine_name:
        # If we have a cuisine name, find dishes based on cuisine
        cuisine_dishes = list(dishcollection.find({"cuisine": {'$regex': cuisine_name, '$options': 'i'}}))
        #print(f"Dishes found for cuisine '{cuisine_name}': {cuisine_dishes}")
        dishes.extend(cuisine_dishes)

    if general_name:
        # If we have a general name, find dishes based on general category
        general_dishes = list(dishcollection.find({"general": {'$regex': general_name, '$options': 'i'}}))
        #print(f"Dishes found for general '{general_name}': {general_dishes}")
        dishes.extend(general_dishes)

    # Remove duplicates if necessary
    dishes = list({dish['_id']: dish for dish in dishes}.values())

    # Check if dishes were found
    if not dishes:
        error_message = f"No dishes found for {category_name or cuisine_name or general_name}."

    return render(request, 'category_dishes.html', {
        'dishes': dishes,
        'category_name': category_name,
        'cuisine_name': cuisine_name,
        'general_name': general_name,  # Add general_name to context
        'error_message': error_message,
    })
