from django.shortcuts import render,redirect
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['allproducts'] = Product.objects.all().order_by('-id')

        return context

class AllproductsView(TemplateView):
    template_name = 'allproducts.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context

class ProductdetailView(TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        p = Product.objects.get(slug = url_slug)
        context['product'] = p
        return context

class AddtocartView(TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from url
        product_id = self.kwargs['pro_id']
        #get product
        product_obj = Product.objects.get(id = product_id)
        #check cart already exists
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id =cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate = product_obj.selling_price, quantity=1,
                    subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            
        
        return context

class MycartView(TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class ManagecartView(View):
    def get(self,request,*args,**kwargs): 
    
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('ecomapp:mycart')

class EmptycartView(View):
    def get(self,request,*args,**kwargs):
        cart_id = request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()

        return redirect('ecomapp:mycart')

class CheckoutView(CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('ecomapp:home')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'order received'
        else:
            return redirect('ecomapp:home')
        return super().form_valid(form)

class CustomerregistrationView(CreateView):
    template_name = 'customerregistration.html'
    form_class = CustomerregistrationForm
    success_url = reverse_lazy('ecomapp:home')

    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username,password,email)
        form.instance.user = user
        login(self.request,user)

        return super().form_valid(form)

class CustomerlogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('ecomapp:home')

class CustomerloginView(FormView):
    template_name = 'customerlogin.html'
    form_class = CustomerloginForm
    success_url = reverse_lazy('ecomapp:home')

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        try:
            user = User.objects.get(username=uname)
            usr = authenticate(username = uname, password= pword)
            try:
                if user is not None and user.customer:
                    login(self.request, usr)
                else:
                    return render(self.request, self.template_name, {'form':self.form_class, 'error': 'Invalid information'})
            except:
                return render(self.request, self.template_name, {'form':self.form_class, 'error': 'Invalid information'})
        except:
            return render(self.request, self.template_name, {'form':self.form_class, 'error': 'Invalid information'})

        return super().form_valid(form)

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'