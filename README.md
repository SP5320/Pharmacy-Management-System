# Tutorial: Pharmacy-Management-System

This project is a **Pharmacy Management System** built with Django.
Its main purpose is to help manage **medicine inventory** and track **sales records**.
Users can sign up, log in, add new medicines, view and update inventory stock,
record medicine sales, and see a history of all transactions, with features for **searching** and **filtering** data.

### Check out the live website here: [Pharmacy Management System](https://shubhampawar.pythonanywhere.com/)

## Visual Overview

```mermaid
flowchart TD
    A0["Django Project Settings
"]
    A1["Django Application (App)
"]
    A2["Database Models
"]
    A3["Views
"]
    A4["URL Routing
"]
    A5["Forms
"]
    A6["Authentication
"]
    A7["Data Filtering
"]
    A0 -- "Includes App" --> A1
    A0 -- "Configures Auth" --> A6
    A1 -- "Contains Models" --> A2
    A1 -- "Contains Views" --> A3
    A1 -- "Contains URLs" --> A4
    A1 -- "Contains Forms" --> A5
    A1 -- "Contains Filters" --> A7
    A4 -- "Routes To Views" --> A3
    A3 -- "Uses Models" --> A2
    A3 -- "Processes Forms" --> A5
    A3 -- "Requires Auth" --> A6
    A3 -- "Applies Filters" --> A7
    A2 -- "Forms Based On" --> A5
    A2 -- "Filters Use" --> A7
    A4 -- "Includes Auth URLs" --> A6
```

## Chapters

1. [Database Models
](01_database_models_.md)
2. [Django Application (App)
](02_django_application__app__.md)
3. [Django Project Settings
](03_django_project_settings_.md)
4. [Forms
](04_forms_.md)
5. [Views
](05_views_.md)
6. [URL Routing
](06_url_routing_.md)
7. [Authentication
](07_authentication_.md)
8. [Data Filtering
](08_data_filtering_.md)
