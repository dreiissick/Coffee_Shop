from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from decimal import Decimal, InvalidOperation
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from Base_App.models import AboutUs, ItemList, Items, Delivery, Cart, CartItem, Order

# Create your views here.

def HomeView(request):
    items = Items.objects.all()  # Get all items
    list = ItemList.objects.all()  # Get all item lists
    return render(request, 'home.html', {'items': items, 'list': list})


# Submit order
def submit_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])  # Retrieve cart from session
        delivery_address = request.POST['delivery_address']  # Get delivery address from form
        phone_number = request.POST['phone_number']  # Get phone number from form

        if not cart:  # Check if cart is empty
            messages.error(request, "Your cart is empty.")
            return redirect('CartView')  # Go back to cart view if empty

        # Save the order to the Delivery model
        for item in cart:
            Delivery.objects.create(
                item_name=item['name'],  # Save item name
                quantity=item['quantity'],  # Save quantity
                price=item['price'],  # Save item price
                delivery_address=delivery_address,  # Save the address
                phone_number=phone_number  # Save phone number
            )

        # Clear the cart from session after placing the order
        request.session['cart'] = []

        # Show success message and redirect to success page
        messages.success(request, "Your order has been placed successfully!")
        return redirect('delivery_success')  # Redirect to success page

    return HttpResponse(status=400)  # Return error response if not a POST request

def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html', {'data': data})

def Menu(request):
    items = Items.objects.all()
    list = ItemList.objects.all()
    return render(request, 'menu.html', {'items': items, 'list': list})

# Delivery form view
def DeliveryView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('user_email')
        address = request.POST.get('address')
        delivery_time = request.POST.get('delivery_time')
        total_amount = request.POST.get('total_amount')

        # Validation for the form
        if name != '' and len(phone_number) == 10 and email != '' and address != '' and delivery_time != '' and total_amount != '':
            # Save the data to the database
            data = Delivery(
                Name=name,
                Phone_number=phone_number,
                Email=email,
                Address=address,
                Delivery_time=delivery_time,
                Total_amount=total_amount
            )
            data.save()

            # Show a success message to the user
            messages.success(request, "Your coffee shop delivery has been successfully booked!")

            # Redirect to the success page
            return redirect('delivery_success')  # Use the URL name of the success page
        else:
            # Show an error message if validation fails
            messages.error(request, "Please fill out all fields correctly.")

    return render(request, 'order_delivery.html')

def DeliverySuccessView(request):
    return render(request, 'delivery_success.html')

def Menu(request):
    items = Items.objects.all()
    item_list = ItemList.objects.all()
    
    # Add debugging
    for item in items:
        print(f"Item: {item.Item_name}, Image: {item.Image}")  # Use the correct attribute names
    
    return render(request, 'menu.html', {'items': items, 'list': item_list})

# Get or create a cart object from session
def get_or_create_cart(request):
    if request.user.is_authenticated:
        # If the user is logged in, use their cart
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    else:
        # If the user is not logged in, use the session to store the cart
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create(is_active=True)  # Ensure 'is_active' is True for session-based cart
            request.session['cart_id'] = cart.id

    return cart

# Add an item to the cart
def add_to_cart(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        item=item, 
        defaults={'quantity': 1, 'price': item.Price}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('Menu')  

# View the cart items
def CartView(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
  
    try:
       
        cart_total = sum(item.item.Price * item.quantity for item in cart_items)
    except:
       
        cart_total = 0
        for item in cart_items:
           
            if hasattr(item, 'price') and item.price:
                cart_total += item.price * item.quantity
            elif hasattr(item.item, 'Price'):
                cart_total += item.item.Price * item.quantity
            elif hasattr(item.item, 'price'):
                cart_total += item.item.price * item.quantity
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def increase_quantity(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(Items, id=item_id)
    cart_item = get_object_or_404(CartItem, cart=cart, item=item)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

# Decrease the quantity of an item in the cart
def decrease_quantity(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(Items, id=item_id)
    cart_item = get_object_or_404(CartItem, cart=cart, item=item)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart_view')

# Remove an item from the cart
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(Items, id=item_id)
    CartItem.objects.filter(cart=cart, item=item).delete()
    return redirect('Cart')

# Clear the entire cart
def clear_cart(request):
    if request.session.get('cart_id'):
        cart = get_or_create_cart(request)
        CartItem.objects.filter(cart=cart).delete()
    return redirect('Cart')

# Placeholder for checkout page
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.item.Price * item.quantity for item in cart_items)
    
    # Debugging log to check if cart items are added to the cart
    print(f"Cart contains {len(cart_items)} items.")  # Debugging log
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})

def increase_quantity(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, item__id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('Cart')

def decrease_quantity(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, item__id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('Cart')

@csrf_exempt
def process_order(request):
    if request.method == 'POST':
        # GET DATA FROM THE FORM
        name = request.POST.get('name')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        items = request.POST.get('items')
        total = request.POST.get('cart_total')
        
        # VALIDATE TOTAL AND CREATE DELIVERY
        if total is None:
            return HttpResponse("Cart total is missing", status=400)
        
        try:
            total = Decimal(total)
        except (InvalidOperation, ValueError):
            return HttpResponse("Invalid total amount", status=400)

        delivery = Delivery(
            name=name,
            address=address,
            payment_method=payment_method,
            items=items,
            total=total
        )
        delivery.save()

        if request.user.is_authenticated:
    # Assuming you're storing cart items in the Cart model
            Cart.objects.filter(user=request.user).delete()   # CLEAR THE CART IN THE SESSION
            
        # PASS DELIVERY DATA TO THE TEMPLATE
        return redirect('order_confirmation', delivery_id=delivery.id)

    return HttpResponse("Invalid request method", status=405)
    

def order_confirmation(request, delivery_id):
    try:
        delivery = Delivery.objects.get(id=delivery_id)
        print(f"Delivery data: {delivery.name}, {delivery.address}")  # Debugging log
    except Delivery.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    return render(request, 'order_confirmation.html', {'delivery': delivery})


def generate_receipt(request, delivery_id):
    try:
        # FETCH THE DELIVERY DATA BASED ON THE DELIVERY ID
        delivery = Delivery.objects.get(id=delivery_id)
    except Delivery.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # CREATE A BYTESIO OBJECT TO STORE THE PDF IN MEMORY
    buffer = BytesIO()
    
    # CREATE THE PDF OBJECT
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # ADD SOME CONTENT TO THE PDF (DELIVERY DETAILS)
    p.drawString(100, 750, f"Order ID: {delivery.id}")
    p.drawString(100, 730, f"Customer Name: {delivery.name}")
    p.drawString(100, 710, f"Address: {delivery.address}")
    p.drawString(100, 690, f"Items: {delivery.items}")
    p.drawString(100, 670, f"Total: ${delivery.total}")
    
    # SAVE THE PDF INTO THE BUFFER
    p.showPage()
    p.save()

    # RESET THE BUFFER'S POSITION TO THE BEGINNING
    buffer.seek(0)

    # CREATE AN HTTP RESPONSE WITH THE PDF FILE FOR DOWNLOAD
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{delivery.id}.pdf"'
    
    return response