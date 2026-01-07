from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Account

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Account,ClientProfile

def client_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('contactNo')
        password = request.POST.get('password')

        # Server-side validation
        if not all([first_name, last_name, email, phone_number, password]):
            messages.error(request, "All fields are required")
            return redirect('client_register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect('client_register')

        if Account.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('client_register')

        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email.split('@')[0],
            email=email,
            password=password
        )

        user.phone_number = phone_number
        user.is_client = True
        user.is_active = True
        user.save()

        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('client_login')

    return render(request, 'client/register.html')


from django.contrib import messages, auth
from django.shortcuts import render, redirect


def client_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            # ✅ CHECK ROLE
            if getattr(user, "is_client", False):
                auth.login(request, user)
                messages.success(request, "Login successful!")
                return redirect("client_dashboard")
            else:
                messages.error(request, "You are not authorized to login as a client.")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "client/login.html")




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ClientProfile

@login_required
def client_profile_view(request):
    profile, created = ClientProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'client/profile.html',   # 🔴 make sure filename matches
        {
            'profile': profile,
            'user': request.user,
        }
    )



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ClientProfileForm

@login_required
def save_client_profile(request):
    profile, created = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect('client_profile')
    else:
        form = ClientProfileForm(instance=profile)

    return render(request, 'client/edit_profile.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Account, VendorDetails
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .models import Account, VendorDetails


def vendor_register(request):
    if request.method == "POST":

        # -------- Account fields --------
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # -------- Vendor fields --------
        company_name = request.POST.get("business_name")
        business_address = request.POST.get("address")

        # OPTIONAL location fields (may be empty)
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        # Contact person
        contact_person = f"{first_name} {last_name}"
        alternate_phone = phone

        # -------- Validation --------
        if not all([first_name, last_name, email, phone, password]):
            messages.error(request, "Account fields are missing.")
            return redirect("vendor_register")

        if not all([company_name, business_address]):
            messages.error(request, "Vendor details are missing.")
            return redirect("vendor_register")

        if Account.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("vendor_register")

        # -------- Create Account --------
        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email.split("@")[0],
            email=email,
            password=password
        )

        user.phone_number = phone
        user.is_vendor = True
        user.is_active = True
        user.save()

        # -------- Create VendorDetails --------
        VendorDetails.objects.create(
            user=user,
            company_name=company_name,
            business_address=business_address,
            contact_person=contact_person,
            alternate_phone=alternate_phone,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            is_verified = True,
        )

        login(request, user)
        messages.success(request, "Vendor registered successfully.")
        return redirect("home")

    return render(request, "vendor/register.html")

def vendor_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            if getattr(user, "is_vendor", False):   # 👈 HERE
                auth.login(request, user)
                messages.success(request, "Vendor login successful!")
                return redirect("vendor_dashboard")
            else:
                messages.error(request, "You are not authorized as a vendor.")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "vendor/login.html")


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home') 

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import CollectorProfile

User = get_user_model()

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import CollectorProfile

User = get_user_model()


def collector_register(request):
    if request.method == 'POST':

        # -------- Account fields --------
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # -------- Collector fields --------
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        profile_photo = request.FILES.get('profilePhoto')
        id_proof = request.FILES.get('idProof')

        # -------- Basic validation --------
        if not all([first_name, last_name, email, phone_number, password]):
            messages.error(request, "All fields are required")
            return redirect('collector_register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('collector_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('collector_register')

        try:
            with transaction.atomic():

                # -------- Create Account --------
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=email,  # safest unique value
                    email=email,
                    password=password
                )

                user.phone_number = phone_number
                user.is_collector = True
                user.is_active = False
                user.save()

                # -------- Create Collector Profile --------
                CollectorProfile.objects.create(
                    user=user,
                    date_of_birth=dob,
                    address=address,
                    profile_photo=profile_photo,
                    id_proof=id_proof
                )

                messages.success(
                    request,
                    "Registration successful. Awaiting admin approval."
                )
                return redirect('home')

        except Exception as e:
            print("REGISTRATION ERROR:", e)  # 👈 VERY IMPORTANT FOR DEBUG
            messages.error(request, "Registration failed. Please try again.")
            return redirect('collector_register')

    return render(request, 'collector/register.html')

def collector_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect('collector_dashboard')  # <-- change to your desired URL
        else:
            messages.error(request, "Invalid email or password")

        
    return render(request, 'collector/login.html')