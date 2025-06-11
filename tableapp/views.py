from django.shortcuts import render
from django.http import HttpResponse
from .models import Vendors,Menu, Category, Item, Category_Item, Tables, Cart, Cart_Item, Orders, Subscription
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import MenuForm, CategoryForm, ItemForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
import io
import base64
# Create your views here.

"""
unique(element, element1)
Helper function that merges unique items from one list into another.

Parameters:
- element: Source list containing items to be added
- element1: Target list to which unique items will be added

Returns:
- Updated element1 list with unique items from both lists
"""
def unique(element, element1):
    for i in element:
        if i in element1:
            continue
        #appends to the unique list if the element is not found
        element1.append(i)
    return element1

"""
check(vendor, name, url)
Validates if a menu name or URL is unique for a specific vendor.

Parameters:
- vendor: Vendor object for which to check the menu uniqueness
- name: The menu name to check
- url: The menu URL to check

Returns:
- True if both the name and URL are unique for the vendor
- False if either the name or URL already exists
"""
def check(vendor, name, url):
    #get all the menus of a vendor
    Menus = Menu.objects.filter(vendor_id=vendor) 
    for entity in Menus:
        if entity.menu_name == name or entity.menu_url == url:
            return False
    return True

"""
check_category(pk, category_name, category_url)
Validates if a category name or URL is unique within a specific menu.

Parameters:
- pk: Primary key of the menu
- category_name: The category name to check
- category_url: The category URL to check

Returns:
- True if both the name and URL are unique for the menu
- False if either the name or URL already exists
"""
def check_category(pk, category_name, category_url):
    menu = Menu.objects.get(pk=pk)
    #get all the categories of a menu
    categorys = Category.objects.filter(menu_id=menu)
    for category in categorys:
        if category.category_name == category_name or category.category_url == category_url:
            return False
    return True

"""
index(request)
Renders the application's homepage.

Parameters:
- request: HTTP request object

Returns:
- Rendered index.html template
"""
def index(request):
    return render(request, "index.html")

"""
signup(request)
Handles user registration and vendor creation.

Parameters:
- request: HTTP request object containing registration data

Process:
1. If POST request, extracts username, password, and email
2. Checks if username already exists
3. Creates a new Django User and corresponding Vendor
4. Redirects to login page on success

Returns:
- On GET: Rendered signup form
- On POST success: Rendered login page
- On username conflict: Redirects back to signup with error
"""
def signup(request):
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        #check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Signup: Username already exists.")
            return redirect("signup")
        #create a new user with a unique username
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        new_vendor = Vendors(user=user)
        new_vendor.save()
        return render(request,"login.html")
    return render(request,"signup.html")

"""
login_view(request)
Authenticates users and initiates their session.

Parameters:
- request: HTTP request object containing login credentials

Process:
1. If POST request, extracts username and password
2. Attempts to authenticate the user
3. Logs in the user if authentication succeeds
4. Redirects to menu dashboard on success

Returns:
- On GET: Rendered login form
- On POST success: Redirect to menu dashboard
- On authentication failure: Login page with error message
"""
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        #use the built in authentication to authenticate the user
        user = authenticate(request, username=username, password=password)
        #if the credentials match
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            context = {"error": "Invalid username or password."}
            return render(request, "login.html", context)

    return render(request, "login.html")

"""
dashboard_signup(request)
Displays the menu management dashboard and handles menu creation.

Parameters:
- request: HTTP request object

Process:
1. Retrieves the vendor associated with the current user
2. If POST request, processes menu creation form
3. Validates menu name and URL uniqueness
4. Creates a new menu if validation passes
5. If GET request, displays existing menus or the "no menu" page

Returns:
- On GET with existing menus: "menuAvailable.html" with menus
- On GET with no menus: "nomenuAvailable.html" with empty form
- On POST: Redirect to menu dashboard with success/error message

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def dashboard_signup(request):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    #creates a new menu
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            #get all the form imput values
            name = form.cleaned_data['menu_name']
            url = form.cleaned_data['menu_url']
            image = form.cleaned_data['image_field']
            #check if the form with a name or url exists
            if check(vendor, name, url):
                menu = Menu(menu_name=name, menu_url=url, image_field=image, vendor_id=vendor)
                menu.save()
                messages.success(request, "Menu: The menu has been created successfully")
            else:
                messages.error(request, "Menu: The menu with the given name or url already exists")
            #send a get request to the same url
            return redirect('menu')
    else:
        #get all the menus corresponding to a vendor
        menus = Menu.objects.filter(vendor_id=vendor)
        if menus:
            return render(request,"menuAvailable.html", {"username":username, "form":MenuForm(), "menus":menus})
        else:
            return render(request, "nomenuAvailable.html", {"username": username, "form":MenuForm()})

"""
delete_menu(request, pk)
Deletes a specific menu.

Parameters:
- request: HTTP request object
- pk: Primary key of the menu to delete

Process:
1. Retrieves the menu object using the primary key
2. Deletes the menu if POST request
3. Displays success message

Returns:
- Redirect to menu dashboard

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def delete_menu(request, pk):
    #get the menu
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu.delete()
        messages.success(request, "Menu: Menu deleted successfully")
        #redirect to the dashboard displaying menus
        return redirect('menu')


"""
edit_menu(request, pk)
Updates an existing menu's details.

Parameters:
- request: HTTP request object containing updated menu data
- pk: Primary key of the menu to edit

Process:
1. Retrieves the menu object using the primary key
2. If POST request, extracts updated name, URL, and optional image
3. Validates that name and URL don't conflict with other menus
4. Updates menu information if validation passes

Returns:
- Redirect to menu dashboard with success/error message

Requires:
- User authentication
"""
@login_required(login_url='/tabletap/login/')
def edit_menu(request, pk):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        new_name = request.POST.get("menu_name")
        new_url = request.POST.get("menu_url")
        # Check if name or url already exists for OTHER menus (exclude this one)
        Menus = Menu.objects.filter(vendor_id=vendor).exclude(id=pk)
        for entity in Menus:
            if entity.menu_name == new_name or entity.menu_url == new_url:
                messages.error(request, "Menu: The menu with the given name or url already exists")
                return redirect('menu')
        # If no conflict, update
        menu.menu_name = new_name
        menu.menu_url = new_url
        #if the user has uploaded a new image, use that or use the previous one
        menu_image = request.FILES.get("image_field")
        if menu_image:
            menu.image_field = menu_image
        menu.save()
        messages.success(request, "Menu: The menu has been edited successfully")
        #redirect to the menu dashboard
        return redirect('menu')

@login_required(login_url='/tabletap/login/')
def subscription(request):
    vendor = Vendors.objects.get(user=request.user)
    subscription = Subscription.objects.filter(vendor=vendor).first()

    if request.method == "POST":
        if "subscribe" in request.POST:
            if not subscription:
                subscription = Subscription(vendor=vendor)
            subscription.is_archived = False
            subscription.save()

        elif "cancel" in request.POST and subscription:
            subscription.is_archived = True
            subscription.save()

        return redirect('get_subscriptions')  # Recommended to redirect back to the same page

    value = subscription is not None and not subscription.is_archived
    return render(request, "subscriptions.html", {"value": value, "subscribe": subscription})


"""
dashboard_category(request, menu_url, pk)
Displays category management dashboard and handles category creation.

Parameters:
- request: HTTP request object
- menu_url: URL segment of the menu
- pk: Primary key of the menu

Process:
1. If GET request, displays existing categories or the "no category" page
2. If POST request, processes category creation form
3. Validates category name and URL uniqueness within the menu
4. Creates a new category if validation passes

Returns:
- On GET with categories: "categoryAvailable.html" with categories
- On GET with no categories: "nocategoryAvailable.html" with empty form
- On POST: Redirect to category dashboard with success/error message

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def dashboard_category(request, menu_url, pk):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    if request.method == "GET":
        #get all the categories corresponding to a menu ti be displayed
        category = Category.objects.filter(menu_id=pk)
        if category:
            return render(request, "categoryAvailable.html", {"username": username, "form":CategoryForm(), "categorys":category,  "menu":Menu.objects.get(id=pk)})
        return render(request, "nocategoryAvailable.html", {"username": username, "form":CategoryForm(), "menu":Menu.objects.get(id=pk)})
    elif request.method == "POST":
        #create a new category
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['category_name']
            url = form.cleaned_data['category_url']
            image = form.cleaned_data['category_image']
            #if the category with a name or url exists
            if  check_category(pk, name, url):
                category = Category(category_name=name, category_url=url, category_image=image, menu_id=Menu.objects.get(id=pk))
                category.save()
                messages.success(request, "Category: The category has been created successfully")
            else:
                messages.error(request, "Category: The category with the name or the url already exists")
            #send a get request to display all the categories corresponding to a menu
            #the menu url in this case does not start or end with "/"
            return redirect("menu_category", menu_url=menu_url, pk=pk)

"""
delete_category(request)
Deletes a specific category.

Parameters:
- request: HTTP request object containing category ID

Process:
1. Extracts category ID from POST data
2. Retrieves the category object
3. Deletes the category
4. Displays success message

Returns:
- Redirect to category dashboard

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def delete_category(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        #menu url is required as a part of the url for the category
        menu = category.menu_id
        category.delete()
        messages.success(request, "Category: Category deleted successfully")
        # The menu URL is stored in the database with slashes (e.g., "/abc/"),
        # but we need it without slashes (e.g., "abc") when used in URL paths.
        return redirect("menu_category", menu_url=menu.menu_url[1:-1], pk=menu.id)


"""
edit_category(request)
Updates an existing category's details.

Parameters:
- request: HTTP request object containing updated category data

Process:
1. Extracts category ID and retrieves the category object
2. Extracts updated name, URL, and optional image
3. Validates that name and URL don't conflict with other categories
4. Updates category information if validation passes

Returns:
- Redirect to category dashboard with success/error message

Requires:
- User authentication
"""
@login_required(login_url='/tabletap/login/')
def edit_category(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        menu = category.menu_id
        new_name = request.POST.get("category_name")
        new_url = request.POST.get("category_url")
        # Check for conflicts in the same menu, excluding current category
        other_categories = Category.objects.filter(menu_id=menu).exclude(id=category_id)
        for entity in other_categories:
            # make sure another category does not exist within the menu
            if entity.category_name == new_name or entity.category_url == new_url:
                messages.error(request, "Category: A category with the given name or url already exists.")
                return redirect("menu_category", menu_url=menu.menu_url[1:-1], pk=menu.id)
        # No conflicts, safe to update
        category.category_name = new_name
        category.category_url = new_url
        if 'category_image' in request.FILES:
            category.category_image = request.FILES['category_image']
        category.save()
        messages.success(request, "Category: The category has been edited successfully.")
        return redirect("menu_category", menu_url=menu.menu_url[1:-1], pk=menu.id)

"""
dashboard_item(request, category_url, pk)
Displays item management dashboard and handles item creation.

Parameters:
- request: HTTP request object
- category_url: URL segment of the category
- pk: Primary key of the category

Process:
1. If GET request, displays existing items or the "no items" page
2. If POST request, processes item creation form
3. Validates item name uniqueness within the menu
4. Creates a new item and associates it with the category if validation passes

Returns:
- On GET with items: "itemsAvailable.html" with items
- On GET with no items: "noitemsAvailable.html" with empty form
- On POST: Redirect to item dashboard with success/error message

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def dashboard_item(request, category_url, pk):
    vendor = Vendors.objects.get(user=request.user) 
    category = Category.objects.get(id=pk)
    menu = category.menu_id
    username = vendor.user.username
    if request.method == "GET":
        #get all the category items corresponding to a category
        category_items = Category_Item.objects.filter(category=category)
        print(category_items)
        #get all the items corresponding to a category
        if category_items:
            items = []
            for category_item in category_items:
                items.append(Item.objects.get(id=category_item.item_id))
            return render(request,"itemsAvailable.html", {"username": username, "category":category, "menu_url":menu.menu_url[1:-1], "menu_id": menu.id , "form":ItemForm(), "items":unique(items, [])})
        else:
            return render(request, "noitemsAvailable.html",  {"username": username, "category":category, "menu_url":menu.menu_url[1:-1], "menu_id": menu.id , "form":ItemForm()})
    elif request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            pricing = form.cleaned_data['pricing']
            description = form.cleaned_data['description']
            name = form.cleaned_data['item_name']
            image = form.cleaned_data['item_image']
            existing_items_in_menu = [] # get all the items within a menu
            categorys = Category.objects.filter(menu_id=menu)
            for cat in categorys:
                cat_items = Category_Item.objects.filter(category=cat)
                for cat_item in cat_items:
                    #get all the existing items in the menu
                    existing_items_in_menu.append(Item.objects.get(id=cat_item.item.id))
            for item_check in existing_items_in_menu:
                #check if an item exists in the menu within a name
                if item_check.item_name == name:
                    messages.error(request, "Item: An item with the given name already exists in this menu.")
                    return redirect("menu_items", category_url=category_url, pk=pk)
            #create an entry in the item and category_item table
            item = Item(item_name=name, item_image=image, description=description, pricing=pricing)
            item.save()
            category_item = Category_Item(category=category, item=item)
            category_item.save()
            messages.success(request, "Item: The item has been created successfully.")
            return redirect("menu_items", category_url=category_url, pk=pk)

"""
delete_item(request)
Deletes a specific item or its association with a category.

Parameters:
- request: HTTP request object containing item and category IDs

Process:
1. Extracts item ID and category ID from POST data
2. Removes the association between the item and category
3. If item is not associated with any other category, deletes the item
4. Displays success message

Returns:
- Redirect to item dashboard

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def delete_item(request):
    if request.method =="POST":
        #get that item
        item_id = request.POST.get("item_id")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        item = get_object_or_404(Item, pk=item_id)
        category_item = get_object_or_404(Category_Item, category=category, item=item)
        #delete the entry from category item
        category_item.delete()
        category_items = Category_Item.objects.filter(item=item)
        #check if the item is part of any other category
        if not category_items:
            #safe to delete
            item.delete()
        messages.success(request, "Item: Item deleted successfully.")
        return redirect("menu_items", category_url=category.category_url[1:-1],pk=category_id)

"""
edit_item(request)
Updates an existing item's details.

Parameters:
- request: HTTP request object containing updated item data

Process:
1. Extracts item ID, category ID, and retrieves the objects
2. Extracts updated name, pricing, description, and optional image
3. Validates that name doesn't conflict with other items in the menu
4. Updates item information if validation passes

Returns:
- Redirect to item dashboard with success/error message

Requires:
- User authentication
"""


@login_required(login_url = '/tabletap/login/')
def edit_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        category_id = request.POST.get("category")
        item = get_object_or_404(Item, pk=item_id)
        category = get_object_or_404(Category, pk=category_id)
        menu = category.menu_id
        new_name = request.POST.get("item_name")
        pricing = request.POST.get("pricing")
        description = request.POST.get("description")
        # Check if item name exists in the menu excluding the current item
        existing_items_in_menu = []
        categorys = Category.objects.filter(menu_id=menu)
        for cat in categorys:
            cat_items = Category_Item.objects.filter(category=cat)
            for cat_item in cat_items:
                existing_items_in_menu.append(Item.objects.get(id=cat_item.item.id))
        for item_check in existing_items_in_menu:
            if item_check.item_name == new_name and item_check.id != item.id:
                messages.error(request, "Item: Another item with the given name already exists in this menu.")
                return redirect("menu_items", category_url=category.category_url[1:-1], pk=category_id)
        # Safe to update
        item.item_name = new_name
        item.pricing = pricing
        item.description = description
        if 'item_image' in request.FILES:
            item.item_image = request.FILES['item_image']
        item.save()
        messages.success(request, "Item: The item has been edited successfully.")
        return redirect("menu_items", category_url=category.category_url[1:-1], pk=category_id)


"""
display_items(request, pk)
Displays all items that can be added to a specific category.

Parameters:
- request: HTTP request object
- pk: Primary key of the category

Process:
1. Retrieves items already in the category
2. Retrieves all items in the menu
3. Filters to show only items not yet in the category

Returns:
- Rendered "allItems.html" with available items

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def display_items(request, pk):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    if request.method == "GET":
        category = get_object_or_404(Category, pk=pk)
        existing_items = []
        for x in Category_Item.objects.filter(category=category):
            existing_items.append(Item.objects.get(id=x.item.id)) #get all the items in a category
        menu = category.menu_id 
        categorys = Category.objects.filter(menu_id=menu) # get all the categories of a menu
        items = []
        for category in categorys:
            category_items = Category_Item.objects.filter(category=category)
            for category_item in category_items:
                items.append(Item.objects.get(id=category_item.item.id)) #get all the items within a menu
        original_items = []
        for y in items:
            if y in existing_items:
                continue
            original_items.append(y) # the elements within a menu but not within the particular category from which the user can select
        #the original items can contain duplicate items so we just pass the unique items
        return render(request, "allItems.html", {"items":unique(original_items,[]), "username":username, "menu":menu, "category":get_object_or_404(Category, pk=pk)}) 

"""
add_existing(request, category, item)
Adds an existing item to a category.

Parameters:
- request: HTTP request object
- category: ID of the category
- item: ID of the item to add

Process:
1. Retrieves category and item objects
2. Creates a Category_Item association
3. Redirects to item dashboard

Returns:
- Redirect to item dashboard

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def add_existing(request, category, item):
    if request.method == "POST":
        category=get_object_or_404(Category, pk=category)
        item=get_object_or_404(Item, pk=item)
        print(category, item)
        #map the existing item to a new category
        #the new item is not created
        category_item = Category_Item(category=category, item=item)
        category_item.save()
        return redirect("menu_items", category_url=category.category_url[1:-1], pk=category.id )

"""
get_qr(request, menu_url, pk)
Generates and displays QR codes for table ordering.

Parameters:
- request: HTTP request object
- menu_url: URL segment of the menu
- pk: Primary key of the menu

Process:
1. If GET request, displays QR code generation form
2. If POST request, deletes existing tables for the menu
3. Creates new tables based on the requested count
4. Generates QR codes for each table with unique URLs
5. Encodes QR codes as base64 for display

Returns:
- On GET: "QR.html" with generation form
- On POST: "GenQR.html" with generated QR codes

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def get_qr(request, menu_url, pk):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    if request.method == "GET":
        return render(request, "QR.html" , {"username": username, "menu_url":menu_url, "pk":pk})
    elif request.method == "POST":
        #delete all the tables corresponding to a menu
        Tables.objects.filter(menu_id=Menu.objects.get(id=pk)).delete()
        total = int(request.POST.get("count"))
        qr_codes = []
        base_url = "https://infs3202-1361da7f.uqcloud.net/tabletap/menu"
        # the table number starts from 1 and ends in total
        for i in range(1, total+1):
            #https://infs3202-1361da7f.uqcloud.net/tabletap/menu/tuesdayg/14/category/1
            full_url = f"{base_url}/{menu_url}/{pk}/category/{i}"
            qr = qrcode.make(full_url)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            # create and save a new table entry to the db, the url always follows the same format
            table = Tables(table_number=i, qr_code_url=full_url, menu_id=Menu.objects.get(id=pk))
            table.save()
            #send the qr codes to be rendered at the frontend
            qr_codes.append({
                'table_number': i,
                'qr_code_base64': img_str,
                'full_url': full_url
            })
        return render(request, "GenQR.html", {"qr_codes": qr_codes, "username": username, "menu_url":menu_url, "pk":pk})

"""
view_order(request)
Displays active orders for the vendor's menus.

Parameters:
- request: HTTP request object

Process:
1. Retrieves all menus belonging to the vendor
2. Retrieves all tables associated with those menus
3. Retrieves all carts associated with those tables
4. Retrieves all active orders from those carts

Returns:
- Rendered "viewOrder.html" with active orders

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def view_order(request):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    #get all the menus of a user
    menus = Menu.objects.filter(vendor_id=vendor)
    #get all the table corresponding to all the menus
    tables = Tables.objects.filter(menu_id__in=menus)
    #get all the carts corresponding to the all the tables
    carts = Cart.objects.filter(table_id__in=tables)
    #get all the orders which are active to be displayed
    #relationships are mapped basically
    orders = Orders.objects.filter(cart_id__in=carts , order_status="active")
    if request.method == "GET":
        return render(request, "viewOrder.html", {"orders":orders})

"""
complete_order(request, order_id)
Marks an order as completed.

Parameters:
- request: HTTP request object
- order_id: ID of the order to complete

Process:
1. Retrieves the order object
2. Updates order status to "completed"
3. Redirects to order view

Returns:
- Redirect to order dashboard

Requires:
- User authentication
"""
@login_required(login_url = '/tabletap/login/')
def complete_order(request, order_id):
    vendor = Vendors.objects.get(user=request.user) 
    username = vendor.user.username
    if request.method == "POST":
        order = get_object_or_404(Orders, pk=order_id)
        #set the order as complete and fill not be displayed on view orders
        order.order_status = "completed"
        order.save()
        return redirect('view_order')

"""
user_dashboard_category(request, menu_url, pk, table_number)
Customer-facing view that displays categories for a menu.

Parameters:
- request: HTTP request object
- menu_url: URL segment of the menu
- pk: Primary key of the menu
- table_number: Table number for the order

Process:
1. Ensures session exists for the user
2. Retrieves or creates an active cart for the session
3. Counts items in the cart
4. Retrieves categories for the menu

Returns:
- Rendered "categoryView.html" with categories and cart info
"""
def user_dashboard_category(request, menu_url, pk, table_number):
    # Ensure session key exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    table = get_object_or_404(Tables, menu_id=pk, table_number=table_number)
    # Get or create the active cart
    cart, created = Cart.objects.get_or_create(
        table_id=table,
        session_key=session_key,
        is_active=True
    )
    Cart_Items = Cart_Item.objects.filter(cart_id=cart)
    print(Cart_Items)
    print(session_key)
    if Cart_Items:
        value = 0
        for cart_item in Cart_Items:
            value += cart_item.quantity
    else:
        value = 0
    if request.method == "GET":
        category = Category.objects.filter(menu_id=pk)
        return render(request, "categoryView.html", {"table": table, "categorys":category, "menu_url":menu_url, "item":value , "menu_id":pk})

"""
user_dashboard_item(request, menu_url, category_id, table_number)
Customer-facing view that displays items for a category.

Parameters:
- request: HTTP request object
- menu_url: URL segment of the menu
- category_id: ID of the category
- table_number: Table number for the order

Process:
1. Retrieves category and associated menu
2. Ensures session exists and cart is active
3. Counts items in the cart
4. Retrieves items for the category

Returns:
- Rendered "itemView.html" with items and cart info
"""
def user_dashboard_item(request, menu_url, category_id, table_number):
    category = Category.objects.get(pk=category_id)
    menu = category.menu_id
    session_key = request.session.session_key
    table = get_object_or_404(Tables, menu_id=menu, table_number=table_number)
    #get the cart for the total number of items to be displayed at the top
    cart = get_object_or_404(Cart, table_id=table, session_key=session_key, is_active=True)
    Cart_Items = Cart_Item.objects.filter(cart_id=cart)
    #if there exists cart items
    if Cart_Items:
        value = 0
        for cart_item in Cart_Items:
            #the quantity of every item in the cart
            value += cart_item.quantity
    else:
        value = 0
    if request.method == "GET":
        category_items = Category_Item.objects.filter(category=category)
        items = [] #items corresponding to a category
        for category_item in category_items:
            items.append(Item.objects.get(id=category_item.item_id))
        return render(request, "itemView.html", {"items":items, "table":table, "category":category ,"id":menu.id,  "item":value})

"""
add_cart_item(request, menu_id, category_id)
Adds an item to the customer's cart.

Parameters:
- request: HTTP request object
- menu_id: ID of the menu
- category_id: ID of the category

Process:
1. Extracts item ID and table number from POST data
2. Retrieves item and table objects
3. Retrieves or creates an active cart for the session
4. Adds item to cart or increments quantity if already present

Returns:
- Redirect to category view
"""
def add_cart_item(request, menu_id, category_id):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        table_number = int(request.POST.get("table_number"))

        item = get_object_or_404(Item, pk=item_id)
        table = get_object_or_404(Tables, menu_id=menu_id, table_number=table_number)

        session_key = request.session.session_key
        # Get or create the active cart
        cart, created = Cart.objects.get_or_create(
            table_id=table,
            session_key=session_key,
            is_active=True #activate the cart for the usage
        )

        # Add or update cart item
        cart_item, item_created = Cart_Item.objects.get_or_create(
            cart_id=cart,
            item_id=item,
            defaults={'quantity': 1} #by default the quantity is set as 1
        )
        #check if the item exists in the cart
        if not item_created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()
        #redirect to the category
        #the menu url does not start or end with "/"
        return redirect("table_menu_category", Menu.objects.get(id=menu_id).menu_url[1:-1], menu_id, table_number)

"""
calculate_sum(items_cart)
Calculates the total price of items in a cart.

Parameters:
- items_cart: List of cart items

Returns:
- Total price (price × quantity) of all items
"""
def calculate_sum(items_cart):
    total = 0
    #all the items in a cartitems
    for x in items_cart:
        #get the pricing of the item and the quantity
        total += x.item_id.pricing * (x.quantity)
    return total

"""
view_cart(request, menu_id, table_id)
Displays the customer's shopping cart.

Parameters:
- request: HTTP request object
- menu_id: ID of the menu
- table_id: ID of the table

Process:
1. Retrieves active cart for the session
2. Retrieves items in the cart
3. Calculates total price

Returns:
- Rendered "ViewCart.html" with cart items and total
"""
def view_cart(request, menu_id, table_id):
    session_key = request.session.session_key
    menu = get_object_or_404(Menu, pk=menu_id)
    if request.method == "GET":
        #get the activce cart corresponding to a table and session
        #there can be multiple carts for the same table with different sessions
        cart = get_object_or_404(Cart, table_id=table_id, session_key=session_key, is_active=True)
        #get the cart items for a particular cart to be dispalyed
        cart_items = Cart_Item.objects.filter(cart_id=cart)
        return render(request, "ViewCart.html", {"cart": cart, "cart_items":cart_items, "menu":menu, "table":get_object_or_404(Tables, id=table_id), "total":calculate_sum(cart_items)})

"""
edit_cart(request, cart_id, item_id, option)
Modifies an item in the customer's cart.

Parameters:
- request: HTTP request object
- cart_id: ID of the cart
- item_id: ID of the item to modify
- option: "delete", "subtract", or "add"

Process:
1. Retrieves cart, item, and cart item objects
2. Performs the requested operation:
   - "delete": Removes item from cart
   - "subtract": Decreases quantity by 1
   - "add": Increases quantity by 1

Returns:
- Redirect to cart view
"""
def edit_cart(request, cart_id, item_id, option):
    session_key = request.session.session_key
    if request.method == "POST":
        cart = get_object_or_404(Cart, pk=cart_id)
        item = get_object_or_404(Item, pk=item_id)
        cart_item = get_object_or_404(Cart_Item, cart_id=cart, item_id=item)
        #if the user clicks on trash button(remmove that cartitem)
        if option == "delete":
            cart_item.delete()
        #if the user clicks on "-"(reduce the quantity by 1)
        elif option == "subtract":
            cart_item.quantity -= 1
            cart_item.save()
        #if the user clicks on "+"(increase quantity by 1)
        elif option == "add":
            cart_item.quantity += 1
            cart_item.save()
        #the user sees the cart again
        return redirect("view_cart", cart.table_id.menu_id.pk, cart.table_id.pk )

"""
checkout(request, cart_id)
Displays the checkout page.

Parameters:
- request: HTTP request object
- cart_id: ID of the cart

Process:
1. Retrieves cart object
2. If POST request, updates allergen notes in the cart

Returns:
- Rendered "Checkout.html" with cart information
"""
def checkout(request, cart_id):
    session_key = request.session.session_key
    if request.method == "POST":
        cart = get_object_or_404(Cart, pk=cart_id)
        allergen = request.POST.get('allergen')
        if allergen:
            cart.notes = allergen
            cart.save()
        return render(request, "Checkout.html", {"table":cart.table_id, "menu":cart.table_id.menu_id , "cart":cart})

"""
submit(request, cart_id)
Processes the final order submission.

Parameters:
- request: HTTP request object
- cart_id: ID of the cart

Process:
1. Retrieves cart object and associated table/menu
2. Extracts customer name, mobile, and email from POST data
3. Calculates total price of cart items
4. Creates a new order with status "active"
5. Marks the cart as inactive

Returns:
- Redirect to category view for new order
"""
def submit(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    table = cart.table_id
    menu = table.menu_id.id
    #url for redirecting the user back to the category with 0 item in cart
    url = table.menu_id.menu_url[1:-1]
    session_key = request.session.session_key
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        #get all the cart items of a cart
        cart_items = Cart_Item.objects.filter(cart_id=cart)
        #the total amount the customer paid
        total = calculate_sum(cart_items)
        order = Orders(cart_id=cart, customer_name=name, customer_phone=mobile, customer_email=email, total_price=total, order_status="active")
        #order submitted, deactivate the cart
        cart.is_active = False
        cart.save()
        order.save()
        #redirect the user back to category
        return redirect("table_menu_category", url, menu, table.table_number)