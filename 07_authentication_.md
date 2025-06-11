# Chapter 7: Authentication

Welcome back! In [Chapter 6: URL Routing](06_url_routing_.md), we learned how Django's navigation system directs web addresses to the correct [Views](05_views_.md). But once a request reaches a view, how do we decide if the person making the request is *allowed* to see the inventory or add a new medicine? We don't want just anyone managing our pharmacy stock!

This is where **Authentication** comes in.

Think of Authentication like the security system for our Pharmacy Management System building. It needs to know:

1.  **Who are you?** (Identification - like showing your ID)
2.  **Are you allowed in?** (Verification - checking if your ID is valid)
3.  **Which parts of the building can you access?** (Authorization - determining permissions, which is a related concept but we'll focus on just *being logged in* for now).

Our project uses Django's powerful built-in authentication system, which handles the common tasks of user accounts: **signing up**, **logging in**, and **logging out**. It also provides easy ways to protect certain pages, making sure only logged-in users can see them.

The goal of this chapter is to understand how our Pharmacy Management System uses Django's authentication features to manage user access and secure important parts of the application, like the inventory list and sales records.

## Django's Built-in Authentication

One of Django's great strengths is that it comes with a ready-to-use authentication system. It's included as a default app when you create a new project.

Remember in [Chapter 3: Django Project Settings](03_django_project_settings_.md), we looked at the `INSTALLED_APPS` list? You'll see these lines there:

```python
# File: pharmacy/settings.py (Snippet)

INSTALLED_APPS = [
    # ... other apps ...
    'django.contrib.auth',         # Django's authentication system
    'django.contrib.contenttypes', # Framework for content types (used by auth)
    # ... other apps ...
]

MIDDLEWARE = [
    # ... other middleware ...
    'django.contrib.sessions.middleware.SessionMiddleware',      # For managing sessions
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Attaches user to request
    'django.contrib.messages.middleware.MessageMiddleware',    # For displaying messages
    # ... other middleware ...
]
```

*   `django.contrib.auth`: This is the core authentication app. It provides user models, permissions, and authentication backend logic.
*   `django.contrib.contenttypes`: Provides a framework for dealing with "types" of installed models, which `django.contrib.auth` uses.
*   `django.contrib.sessions.middleware.SessionMiddleware`: Handles user sessions. When a user logs in, Django starts a session, typically stored using a cookie in the user's browser.
*   `django.contrib.auth.middleware.AuthenticationMiddleware`: This is a crucial piece of middleware. It examines the session data from `SessionMiddleware` and, if a user is logged in, it attaches the corresponding `User` object to the incoming `request` object as `request.user`. This allows you to easily check `request.user.is_authenticated` in your views or templates.

Because these are included by default and enabled in `MIDDLEWARE`, Django handles a lot of the underlying authentication work for us.

## Signing Up (Creating a New User)

Before someone can log in, they need an account. Our system allows new users to sign up.

Django provides a standard `User` model (`django.contrib.auth.models.User`) out-of-the-box. We don't need to define this model in our `store/models.py` because it's part of the built-in auth app.

To create a form for signing up, our project uses a custom form based on Django's `UserCreationForm`. You can see `SignupForm` in `store/forms.py`, although for simplicity, the core functionality of creating a user is similar to using `UserCreationForm` directly.

Let's look at the `signup` view in `store/views.py` that handles the signup process:

```python
# File: store/views.py (Signup Snippet)

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Often used or basis for custom form
from django.contrib import messages
from .forms import SignupForm # Our project's custom form

def signup(request):
    form = SignupForm() # Create an empty form for GET requests
    if request.method == "POST":
        form = SignupForm(request.POST) # Create form with submitted data
        if form.is_valid():
            user = form.save() # Save the new user to the database!
            # Optional: Log the user in immediately after signup
            # login(request, user)
            messages.success(request, "Account Successfully created!")
            return redirect('Login') # Redirect to the login page

    context = {"form":form}
    return render(request, 'store/signup.html', context)
```

*   When a user visits the signup page (`GET` request), an empty `SignupForm` is created and passed to the template (`store/signup.html`) for display.
*   When the user fills out the form and submits it (`POST` request), a `SignupForm` is created with the submitted data (`request.POST`).
*   `form.is_valid()` checks if the username, password, etc., meet the criteria.
*   If valid, `form.save()` (because `SignupForm` is a `ModelForm` or similar, based on the User model) creates a new user object in the database.
*   Finally, the user is redirected to the login page.

The URL pattern for this view is defined in `store/urls.py`:

```python
# File: store/urls.py (Signup Snippet)

from django.urls import path
from . import views # Import views from the store app

urlpatterns = [
    # ... other paths ...
    path("signup/", views.signup, name="Signup"), # Maps /signup/ to the signup view
    # ... other paths ...
]
```

This means a request to `/signup/` (after being routed from the project `urls.py`) will be handled by our `signup` view function.

## Logging In (Verifying Identity)

Logging in is the process where a user proves they are who they claim to be. Our project uses a custom login form and view.

Let's look at the `loginPage` view in `store/views.py`:

```python
# File: store/views.py (Login Snippet)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login # Import authenticate and login functions

def loginPage(request):
    if request.method == "POST":
        # Get username and password directly from the POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's authenticate function to verify credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            # Redirect the user to the page defined by LOGIN_REDIRECT_URL in settings.py
            return redirect('StoreHome') # 'StoreHome' is the URL name defined in urls.py
        else:
            # If authentication fails, show an error message
            msg = "Username or Password is incorrect"
            return render(request, 'store/login.html', {"message":msg})

    # For GET requests, just render the empty login page
    return render(request, 'store/login.html')
```

*   For a `GET` request, the view simply renders the `store/login.html` template, showing an empty login form.
*   For a `POST` request (when the user submits the form), it gets the submitted username and password.
*   `authenticate(request, username=username, password=password)` is a key Django function. It checks the provided credentials against the users in the database. If they match a user, it returns the `User` object; otherwise, it returns `None`.
*   If `authenticate` returns a `User` object, `login(request, user)` is called. This function establishes a session for the user, marking them as logged in for future requests.
*   The user is then redirected to the page named `'StoreHome'`. Where does `'StoreHome'` come from? It's defined in our [Django Project Settings](03_django_project_settings_.md) using `LOGIN_REDIRECT_URL = '/StoreHome'`, and `/StoreHome` is the URL that points to the `index` view via the `store/urls.py` name mapping.

The URL pattern for the login page is in `store/urls.py`:

```python
# File: store/urls.py (Login Snippet)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginPage, name="Login"), # Maps the root path "" to loginPage
    # ... other paths ...
]
```

As we saw in [Chapter 6: URL Routing](06_url_routing_.md), `path("", views.loginPage, name="Login")` in `store/urls.py` means that the root URL `/` is directed to the `loginPage` view. The `name="Login"` is used by the `@login_required` decorator (discussed below) to know where to redirect unauthenticated users.

## Logging Out (Ending the Session)

Logging out simply ends the user's authenticated session.

The `logoutUser` view in `store/views.py` handles this:

```python
# File: store/views.py (Logout Snippet)

from django.shortcuts import render, redirect
from django.contrib.auth import logout # Import the logout function

def logoutUser(request):
    logout(request) # End the user's session
    # Redirect the user to the page defined by LOGOUT_REDIRECT_URL in settings.py
    return redirect('Login') # 'Login' is the URL name defined in urls.py
```

*   `logout(request)` is a built-in Django function that takes the current request, clears the user's session data, and effectively logs them out.
*   The user is then redirected to the page named `'Login'`, as configured by `LOGOUT_REDIRECT_URL = '/Login'` in `settings.py`.

The URL pattern for logout is in `store/urls.py`:

```python
# File: store/urls.py (Logout Snippet)

from django.urls import path
from . import views

urlpatterns = [
    # ... other paths ...
    path("logout/", views.logoutUser, name="Logout"), # Maps /logout/ to logoutUser
    # ... other paths ...
]
```

So, visiting `/logout/` triggers the `logoutUser` view, ending the user's session.

## Protecting Views with `@login_required`

Now that we know how users sign up, log in, and log out, how do we prevent non-logged-in users from seeing sensitive pages like the inventory or records?

This is where the `@login_required` decorator comes in. A **decorator** is a special Python syntax (using the `@` symbol) that wraps around a function (like a view function) to add extra functionality *before* the original function runs.

The `@login_required` decorator checks if the user associated with the `request` object (`request.user`) is authenticated (`request.user.is_authenticated`).

If the user *is* authenticated, the decorated view function runs as normal.
If the user *is not* authenticated, the decorator immediately redirects the user to the login page, preventing them from reaching the view's logic.

Let's look at several views in `store/views.py` that use this decorator:

```python
# File: store/views.py (Protected Views Snippet)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Import the decorator

# ... other imports ...

@login_required(login_url='Login') # Apply the decorator here!
def index(request):
    # This view only runs if the user is logged in
    print(request.user) # Access the logged-in user object
    return render(request, 'store/index.html')

@login_required(login_url='Login') # Protect the about page too
def about(request):
    return render(request, 'store/about.html')

@login_required(login_url='Login') # Protect adding medicine
def addmedicine(request):
    # ... form handling and saving logic ...
    pass # Simplified for example

@login_required(login_url='Login') # Protect viewing inventory
def inventory(request):
    # ... fetching and displaying inventory data ...
    pass # Simplified for example

# ... many other views like sellmedicine, records, update_med, delete_med/rec ...
```

Notice the `@login_required(login_url='Login')` line right above the `def` line for each of these view functions.

*   `@login_required`: This applies the login required check.
*   `(login_url='Login')`: This tells the decorator *where* to send the user if they are *not* logged in. We provide the `name` of the login URL pattern from our `store/urls.py` (`name="Login"`). Django will automatically figure out the correct URL path (`/`).

So, if an unauthenticated user tries to access `/inventory/`, the `@login_required` decorator on the `inventory` view will detect they are not logged in and redirect them to `/`. Only after they successfully log in will they be able to see the inventory page.

This is a very common and simple way to add security to your views!

## How Authentication Works (Simplified Flow)

Let's visualize the flow for a request to a protected page like `/inventory/`:

```mermaid
sequenceDiagram
    participant Browser
    participant DjangoURLs["URL Routing\n(pharmacy/urls.py & store/urls.py)"]
    participant LoginRequired["@login_required\nDecorator"]
    participant AuthenticationMW["Authentication\nMiddleware"]
    participant SessionMW["Session\nMiddleware"]
    participant InventoryView["store.views.inventory"]
    participant Database

    Browser->>AuthenticationMW: HTTP Request /inventory/
    AuthenticationMW->>SessionMW: Reads session cookie
    SessionMW-->>AuthenticationMW: Provides session data (if any)
    AuthenticationMW->>AuthenticationMW: Checks session data
    alt User is NOT logged in
        AuthenticationMW-->>DjangoURLs: Request proceeds (now with request.user = AnonymousUser)
        DjangoURLs->>LoginRequired: Directs /inventory/ to decorator before view
        LoginRequired->>LoginRequired: Checks request.user.is_authenticated
        LoginRequired->>Browser: Redirects to login page (e.g., /)
    else User IS logged in
        AuthenticationMW->>AuthenticationMW: Attaches User object to request (request.user)
        AuthenticationMW-->>DjangoURLs: Request proceeds (now with request.user = User object)
        DjangoURLs->>LoginRequired: Directs /inventory/ to decorator before view
        LoginRequired->>LoginRequired: Checks request.user.is_authenticated (is True)
        LoginRequired-->>InventoryView: Allows request to reach the view
        InventoryView->>Database: Fetches data
        Database-->>InventoryView: Returns data
        InventoryView-->>Browser: Sends Inventory HTML Response
    end
```

This diagram shows how the Middleware first processes the request, allowing `request.user` to be set. Then, if the view has the `@login_required` decorator, it acts as a gatekeeper based on `request.user.is_authenticated` *before* the view's main logic (like fetching data from the database) is executed.

## Summary

In this chapter, we explored **Authentication** in our Pharmacy Management System, learning how Django's built-in features help us manage user access.

*   We understood the core need for authentication: verifying identity to protect parts of the system.
*   We saw how Django's `django.contrib.auth` app and related middleware handle the underlying authentication system, making `request.user` available in views.
*   We looked at the process for **Signing Up** using a form and a view to create new user accounts.
*   We examined the process for **Logging In**, using `authenticate()` to verify credentials and `login()` to establish a user session.
*   We saw how **Logging Out** is handled simply using Django's `logout()` function to end the user's session.
*   Crucially, we learned how the `@login_required` decorator is used on views to automatically restrict access, redirecting unauthenticated users to the login page specified by `login_url`.
*   We briefly traced the request flow for protected views, seeing how the decorator acts as a gatekeeper after middleware has processed the user's session.

Authentication is a fundamental security layer, ensuring that only authorized individuals can access the sensitive operations within the pharmacy system, like managing inventory and viewing records.

With authentication in place, we can now focus on other aspects of displaying and managing data. In the next chapter, we'll look at how to make it easier to find specific information within our potentially large lists of medicines or sales records.

Let's move on to the next chapter: [Data Filtering](08_data_filtering_.md).
