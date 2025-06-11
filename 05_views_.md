# Chapter 5: Views

Welcome back! In our journey building the Pharmacy Management System, we've laid down some crucial foundations:
*   In [Chapter 1: Database Models](01_database_models_.md), we designed the structure for our data – defining what information makes up a `Medicine` and a `Sold` item.
*   In [Chapter 2: Django Application (App)](02_django_application__app__.md), we organized our project into a main `store` app.
*   In [Chapter 3: Django Project Settings](03_django_project_settings_.md), we configured the overall project rules and hooked up our app.
*   In [Chapter 4: Forms](04_forms_.md), we learned how to create forms that users fill out to input data, like adding a new medicine or recording a sale.

Now, how do all these pieces connect when a user actually *uses* the website? When someone clicks a link or types a web address, what happens?

This is where **Views** come in!

Think of your Django project like a restaurant.
*   The [Database Models](01_database_models_.md) are the ingredients – the raw materials you work with.
*   The [Forms](04_forms_.md) are like the order pad the waiter uses to take your request.
*   **Views** are like the chefs in the kitchen. They receive the order (the user's request), look at the ingredients (interact with the Models/database), maybe follow a recipe (perform logic or calculations), use the order details (process Form data), prepare the final dish (generate the web page), and send it back to the waiter (Django) to serve to the customer (the user).

## What are Views?

In Django, a **view** is simply a Python function or class that takes a web request and returns a web response. It's the central hub where you write the logic for handling requests that come to your application.

When you visit a specific web address (URL) in your browser that belongs to your Django project, Django looks up which view function is assigned to that URL and calls it.

A view function typically does the following:

1.  **Receives the `request` object:** This object contains all the information about the incoming request, like the user's browser, the data submitted in a form (`POST` data), or parameters in the URL.
2.  **Performs logic:** This is the core part. The view decides what needs to happen. This might involve:
    *   Fetching data from the database using [Database Models](01_database_models_.md).
    *   Processing data submitted by a user through a [Form](04_forms_.md).
    *   Performing calculations (like calculating a bill).
    *   Checking user permissions ([Authentication](07_authentication_.md)).
3.  **Decides the response:** Based on the logic, the view decides what to send back to the user. This is often:
    *   Rendering an HTML page using a template.
    *   Redirecting the user to another URL.
    *   Returning simple data like a file or text.
4.  **Returns a `response` object:** This object contains the final output (like the HTML content) and other details like headers.

## Our Views in `store/views.py`

All the view functions for our `store` app are located in the `store/views.py` file.

Let's look at a very simple view function from our project:

```python
# File: store/views.py (Snippet)

from django.shortcuts import render
# ... other imports ...

@login_required(login_url='Login') # We'll cover this later in Authentication
def index(request):
    # This view function takes 'request' as input
    print(request.user) # Just for debugging, shows the logged-in user

    # It decides to render an HTML template
    # render() is a shortcut that combines loading a template, filling it with data,
    # and returning an HttpResponse object.
    return render(request, 'store/index.html')

# ... other views ...
```

*   `def index(request):`: This defines a view function named `index`. It takes one argument, `request`, which is the `HttpRequest` object.
*   `return render(request, 'store/index.html')`: This is the most common way views return HTML. The `render` function takes the request, the path to an HTML template (`'store/index.html'`), and optionally a dictionary of data to send to the template. In this case, it just renders the basic home page without extra data.

Another simple example:

```python
# File: store/views.py (Snippet)

from django.shortcuts import render
# ... other imports ...

@login_required(login_url='Login') # Authentication requirement
def about(request):
    # Just render the 'about' page template
    return render(request, 'store/about.html')

# ... other views ...
```

The `about` view is even simpler; it just loads and renders the `store/about.html` template.

These simple views demonstrate the core concept: a function receives a request and returns a response, often by rendering a template.

## Views Handling Data (Models and Forms)

Views are where the interaction with [Database Models](01_database_models_.md) and [Forms](04_forms_.md) happens.

Let's look at the `inventory` view, which needs to fetch data using our `Medicine` model:

```python
# File: store/views.py (Snippet)

from django.shortcuts import render
from store.models import Medicine # Import the Medicine model
from .filters import MedicineFilter # Import the filter form (later chapter)
# ... other imports ...

@login_required(login_url='Login')
def inventory(request):
    # 1. Fetch data from the database using the Medicine model
    # Medicine.objects.all() gets ALL records from the Medicine table
    tdata = Medicine.objects.all()

    # 2. Use a filter (optional, covered later)
    myFilter = MedicineFilter(request.GET, queryset=tdata)
    tdata = myFilter.qs

    # 3. Render the template, passing the fetched data to it
    # The data is passed as a dictionary {'messages': tdata, 'myFilter': myFilter}
    # Inside inventory.html, you can access this data using {{ messages }} etc.
    return render(request, 'store/inventory.html', {"messages": tdata, "myFilter": myFilter})

# ... other views ...
```

Here, the `inventory` view:
1.  Uses `Medicine.objects.all()` to query the database and get all `Medicine` objects. `Medicine.objects` is Django's way of interacting with the `Medicine` table.
2.  (Includes filter logic, which we'll skip for now).
3.  Calls `render` to display the `store/inventory.html` template, and importantly, passes the fetched medicine data (`tdata`) to the template using the key `"messages"`. The template then uses this data to display the inventory list.

This shows how a view fetches data from the [Database Models](01_database_models_.md) and makes it available to the HTML template.

Now, let's revisit the `addmedicine` view, which uses a [Form](04_forms_.md) to handle user input and save data using our `Medicine` model.

```python
# File: store/views.py (Snippet)

from django.shortcuts import render, redirect
from store.models import Medicine # Import the Medicine model
from .forms import AddMedicineForm # Import the AddMedicineForm
# ... other imports ...

@login_required(login_url='Login')
def addmedicine(request):
    # Check if the request is a POST request (form submission)
    if request.method == "POST":
        # Create a form instance, populating it with data from the POST request
        fm = AddMedicineForm(request.POST)

        # Check if the data in the form is valid
        if fm.is_valid():
            # If valid, get the cleaned (processed) data
            med_name = fm.cleaned_data['Medicine_Name']
            cmp_id = fm.cleaned_data['Company_ID']
            # ... get other cleaned data ...
            mfg = fm.cleaned_data['Manufacturing_date']
            exp = fm.cleaned_data['Expiry_date']
            prc = fm.cleaned_data['Price']
            stc = fm.cleaned_data['stock']

            # Create a new Medicine object using the cleaned data
            reg = Medicine(Medicine_Name=med_name, Company_ID=cmp_id, Company_name=fm.cleaned_data['Company_name'], Manufacturing_date=mfg, Expiry_date=exp, Price=prc, stock=stc)

            # Save the new Medicine object to the database
            reg.save()

            # Prepare a new blank form to show the user after successful submission
            fm = AddMedicineForm()
            status_message = "Successfull! Data Added Successfully" # Message to display
            # Render the template again with a blank form and a success message
            return render(request, 'store/addmedicine.html', {"status": status_message, "form": fm})

    # If the request is NOT POST (likely GET, the initial page load)
    else:
        # Create a blank form instance to display
        fm = AddMedicineForm()

    # Render the template, passing the form instance (either blank or with errors)
    return render(request, 'store/addmedicine.html', {'form':fm})

# ... other views ...
```

This `addmedicine` view demonstrates how views handle form submissions:
*   When the page is first loaded (`GET` request), it creates an empty `AddMedicineForm` and renders the template.
*   When the form is submitted (`POST` request), it creates an `AddMedicineForm` using the submitted data (`request.POST`).
*   It calls `fm.is_valid()` to trigger the validation logic (checking data types, required fields, etc.).
*   If valid, it accesses the processed data from `fm.cleaned_data`.
*   It then manually creates a new `Medicine` object using this cleaned data and calls `.save()` on the model object to store it in the database.
*   Finally, it renders the page again, usually either redirecting or showing a fresh form with a success message.

This view clearly shows the chef processing the order (form data), using ingredients (creating a `Medicine` object), and storing it (saving to the database).

## Views Performing Logic (Calculations and Updates)

Views also contain the business logic, like calculations or updating existing data. Let's look at the `sellmedicine` view:

```python
# File: store/views.py (Snippet)

from django.shortcuts import render, redirect
from store.models import Medicine, Sold # Import both models
from .forms import SellMedicineForm # Import the SellMedicineForm
# ... other imports ...

@login_required(login_url='Login')
def sellmedicine(request, Medicine_ID): # Takes Medicine_ID from the URL
    # Get the specific Medicine object being sold using its ID
    pi = Medicine.objects.get(pk=Medicine_ID) # pk stands for primary key

    if request.method == "POST":
        # Create a SellMedicineForm instance with submitted data
        # instance=pi makes the form's initial data the values from the 'pi' Medicine object
        fm = SellMedicineForm(request.POST, instance=pi) # Note: This form is based on 'Sold', but we use instance=pi to pre-fill/link

        if fm.is_valid():
            # Get cleaned data from the form
            prc = fm.cleaned_data['Price']     # Price of medicine
            qty = fm.cleaned_data['Quantity'] # Quantity sold

            # --- Perform Calculation ---
            amt = prc * qty # Calculate the total bill amount!

            # --- Create and Save Sold Record ---
            # Create a new Sold object with cleaned data and the calculated amount
            reg = Sold(
                Person_ID = fm.cleaned_data['Person_ID'],
                Medicine_ID=fm.cleaned_data['Medicine_ID'],
                Medicine_Name=fm.cleaned_data['Medicine_Name'],
                Company_ID=fm.cleaned_data['Company_ID'],
                Company_name=fm.cleaned_data['Company_name'],
                Manufacturing_date=fm.cleaned_data['Manufacturing_date'],
                Expiry_date=fm.cleaned_data['Expiry_date'],
                Price=prc,
                Customer_name=fm.cleaned_data['Customer_name'],
                Phone_number=fm.cleaned_data['Phone_number'],
                Quantity=qty,
                Bill_amount=amt, # Use the calculated amount
                Purchase_date=fm.cleaned_data['Purchase_date']
            )
            reg.save() # Save the new Sold record

            # --- Update Medicine Stock ---
            item = int(qty)
            pi.stock -= item # Subtract sold quantity from the Medicine object's stock
            pi.save()        # Save the updated Medicine object back to the database

            # Redirect after successful sale
            return redirect('Inventory')

    else: # GET request
        # Create a SellMedicineForm instance, pre-filled with data from the Medicine object (pi)
        fm = SellMedicineForm(instance=pi)

    # Render the template, passing the form instance
    return render(request, 'store/sellmedicine.html', {"form": fm})

# ... other views ...
```

The `sellmedicine` view is a great example of comprehensive view logic:
*   It takes a `Medicine_ID` from the URL to know *which* medicine is being sold.
*   It fetches the `Medicine` object from the database using that ID (`Medicine.objects.get(...)`).
*   It handles form submission (`POST`) and validation.
*   Crucially, it performs a calculation: `amt = prc * qty`. The view is where this business logic lives.
*   It creates a new `Sold` object and saves it, including the calculated `Bill_amount`.
*   It updates the stock of the original `Medicine` object (`pi.stock -= item`) and saves the updated object back to the database.
*   Finally, it redirects the user to the inventory page.

## Views in the Request/Response Cycle

Let's visualize where the view fits into the overall process when a user makes a request:

```mermaid
sequenceDiagram
    participant UserBrowser["User's Browser"]
    participant URLDispatcher["Django URL Dispatcher"]
    participant ViewFunction["Your View Function\n(e.g., inventory, addmedicine)"]
    participant AppLogic["Application Logic\n(Models, Forms, Calculations, etc.)"]
    participant TemplateRenderer["Django Template Renderer"]

    UserBrowser->>URLDispatcher: HTTP Request (e.g., GET /inventory/)
    URLDispatcher->>ViewFunction: Calls the assigned view function,\npasses request object
    ViewFunction->>AppLogic: Interacts with Models (fetch data)\nProcesses Forms (validate/save)\nPerforms calculations\n(e.g., Medicine.objects.all(), form.is_valid(), amt=price*qty)
    AppLogic-->>ViewFunction: Returns data or status
    ViewFunction->>TemplateRenderer: Tells Django which template to use\nand passes data to it (e.g., render(request, 'store/inventory.html', {'data': ...}))
    TemplateRenderer->>UserBrowser: Builds and sends back HTTP Response\n(the final HTML page)

```

As you can see, the View Function is right in the middle. It receives the request after the [URL Routing](06_url_routing_.md) figures out which view is needed, interacts with other parts of the application (`AppLogic` which involves [Database Models](01_database_models_.md), [Forms](04_forms_.md), etc.), and then directs the response, often via the `TemplateRenderer` to generate the final HTML.

## Function-Based vs. Class-Based Views (Briefly)

You'll notice all the views in our project are Python functions. These are called **Function-Based Views (FBVs)**. They are straightforward and easy to understand for beginners.

Django also provides **Class-Based Views (CBVs)**, which are Python classes that handle requests. They offer a way to structure views using object-oriented principles and provide built-in generic views for common tasks (like displaying a list of objects, showing details of one object, or handling forms) which can reduce the amount of code you need to write.

For this beginner tutorial and our project's current structure, we will stick to Function-Based Views as they are more explicit about what's happening step-by-step, which is great for learning.

## Summary

In this chapter, we learned that **Views** are the core logic handlers in Django.

*   A view is a Python function that takes a web request and returns a web response.
*   Views are responsible for processing requests, interacting with [Database Models](01_database_models_.md) to fetch or save data, handling user input from [Forms](04_forms_.md), performing business logic like calculations, and deciding what output (usually an HTML page via a template) to return.
*   We saw examples from our `store/views.py` file demonstrating how views render simple pages, fetch data for display (`inventory`), and process form submissions to add (`addmedicine`) or modify (`sellmedicine`) data while performing calculations and updates.
*   Views are the central piece connecting incoming requests to the application's functionality and ultimately generating the response sent back to the user.

Now that we know what views do and how they interact with other parts of the application, the next logical question is: How does Django know *which* view function to call for a specific web address (URL)? This is handled by **URL Routing**.

Let's move on to the next chapter: [URL Routing](06_url_routing_.md).
