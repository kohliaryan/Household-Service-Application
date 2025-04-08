# Household Services Application - V2 🚀

## Overview
The **Household Services Application - V2** is a multi-user platform designed to provide comprehensive home servicing solutions. It enables seamless interaction between three roles: **Admin**, **Service Professionals**, and **Customers**. Built using modern frameworks, the application ensures efficient service management, user authentication, and task automation.

---

## Features 🌟

### Admin Role:
- Root access with no registration required.
- Monitor all users (customers/service professionals).
- Create, update, and delete services.
- Approve service professionals after profile verification.
- Block customers/service professionals based on fraudulent activity or poor reviews.

### Service Professional Role:
- Login/Registration functionality.
- Accept or reject service requests.
- View assigned service requests and update their status.
- Profiles visible to customers based on reviews.

### Customer Role:
- Login/Registration functionality.
- Search and view services by name or location (pin code).
- Create, edit, and close service requests.
- Post reviews/remarks on completed services.

---

## Core Functionalities 🔑

1. **Role-Based Access Control (RBAC)**:
   - Admin, Service Professional, and Customer roles implemented using Flask security or JWT-based authentication.

2. **Admin Dashboard**:
   - Manage users and services.
   - Approve or block users based on activity/reviews.

3. **Service Management**:
   - Admin can create, update, or delete services with attributes like name, price, time required, etc.

4. **Service Requests**:
   - Customers can create, edit, and close service requests.
   - Professionals can accept/reject assigned requests and mark them as completed.

5. **Search Functionality**:
   - Customers can search for services by name or location.
   - Admins can search for professionals for review/blocking purposes.

6. **Scheduled Jobs**:
   - Daily reminders for pending service requests sent via Google Chat Webhooks/SMS/Email.
   - Monthly activity reports emailed to customers with service details.
   - CSV export of closed service requests triggered by the admin.

7. **Performance Optimization**:
   - Caching implemented using Redis to improve API performance with cache expiry.

---

## Frameworks & Libraries Used 🛠️

### Backend:
- **Flask**: For API development and role-based access control.
- **Redis & Celery**: For caching and batch jobs.
- **SQLite**: For database storage.

### Frontend:
- **VueJS**: For dynamic UI development.
- **Bootstrap**: For responsive styling.

### Additional Tools:
- **Google Chat Webhooks/SMS/Email APIs**: For notifications.
- **ChartJS (Optional)**: For creating charts in reports.
