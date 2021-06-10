from ecommerce import app
from flask import render_template, request, session, redirect, jsonify
from ecommerce.controllers.customer_controller import CustomerController
from ecommerce.controllers.category_controller import CategoryController
from ecommerce.controllers.product_controller import ProductController
from ecommerce.controllers.cart_controller import CartController
from ecommerce.controllers.order_controller import OrderController

def render_template_with_nav(html_page, **kwargs):
    categories = CategoryController().index()
    auth = session.get('auth')
    cart = []
    if auth:
        cart = CartController().get(auth[0]['customer_id'])

    return render_template(html_page, title=kwargs.get('title'), showCarousel=kwargs.get('showCarousel'),
                           categories=categories, auth=auth, cart=cart, response=kwargs.get('response'))


@app.route('/')
def home():
    top_3_categories = CategoryController().top_3_categories()
    top_products = ProductController().top_products()
    return render_template_with_nav('customer/home.html', showCarousel=True, response={'top_3_categories': top_3_categories, 'top_products': top_products})


@app.route('/about-us')
def about():
    return render_template_with_nav('customer/about.html', title='About Us')


@app.route('/contact-us')
def contact():
    return render_template_with_nav('customer/contact.html', title='Contact Us')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template_with_nav('customer/auth/login.html', title='Login')
    else:
        customer = CustomerController().login(request.form)
        if customer:
            session['auth'] = customer
            return redirect('/')
        else:
            # 'gringgo1987'
            return render_template_with_nav('customer/auth/login.html', title='Login')



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method=='GET':
        return render_template_with_nav('customer/auth/registration.html', title='Registration')
    else:
        customer = CustomerController().register(request.form)
        if customer:
            session['auth'] = customer
            return redirect('/')
        else:
            return render_template_with_nav('customer/auth/registration.html', title='Registration')



@app.route('/categories/<category_id>')
def categories(category_id):
    category = CategoryController().find_by_id(category_id)
    products = ProductController().product_by_category_id(category_id)
    return render_template_with_nav('customer/categories.html', title=category['product_category_name'], showPageBanner=True, response={'products': products, 'category': category})


@app.route('/products/<product_id>')
def products(product_id):
    product = ProductController().find_by_id(product_id)
    return render_template_with_nav('customer/products.html', title=product['product_name'], response={'product': product})


@app.route('/cart', methods=["GET", "POST"])
def cart():
    if request.method == 'GET':
        return render_template_with_nav('customer/cart.html', title='Cart')
    else:
        data = {'product_id': request.form['product_id'], 'customer_id': session.get('auth')[0]['customer_id']}
        cart = CartController().insert(data)
        return jsonify({"msg": 'success'})


@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    if request.method == 'GET':
        return render_template_with_nav('customer/checkout.html', title='Checkout')
    else:
        customer_id = session.get('auth')[0]['customer_id']
        order_id = OrderController().insert(customer_id)
        return redirect('/thankyou/'+order_id)



@app.route('/search')
def search():
    products = ProductController().search_products(request)
    return render_template_with_nav('customer/search.html', title='Search', response={"products": products})

@app.route('/logout')
def logout():
    session['auth'] = None
    return redirect('/')

@app.route('/remove-cart', methods=["POST"])
def remove_cart():
    CartController().remove(request.form['id'])
    return jsonify({"msg": 'success'})

@app.route('/thankyou/<order_id>')
def thankyou(order_id):
    order = OrderController().get(order_id)
    return render_template_with_nav('customer/thankyou.html', title=thankyou, response={"order": order})
