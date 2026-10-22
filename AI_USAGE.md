
# AI Usage Documentation

## 1. AI Tools Used

- **Tool:** ChatGPT by OpenAI
- **Purpose:** Project planning, Django backend implementation guidance, frontend development, documentation, and testing suggestions.
- **Technologies involved:** Python, Django, Django REST Framework, HTML, CSS, JavaScript, and SQLite.

## 2. Prompts Given

The following prompts summarize the requests used during development:

1. "We operate an ecommerce platform. When a customer places an order, the warehouse team needs to know which shipping box should be used. Each product has dimensions and weight. Each box has internal dimensions, maximum weight capacity, and cost. Your task is to design and build a small Django-based system that recommends the most suitable box for an order."

2. "Next."

   Requested the next development phase, including automated tests and API testing.

3. "We will build frontend using html,js,css."

   Requested a frontend implemented using HTML, CSS, and vanilla JavaScript rather than a JavaScript framework.

4. "Add a readme file to it."

   Requested project documentation covering setup, features, architecture, API usage, and testing.

5. "You may use AI tools, but include an AI_USAGE.md file containing:
   1. Which AI tool(s) you used.
   2. The prompts you gave.
   3. What output you accepted.
   4. What output you rejected or modified.
   5. Any mistakes the AI made.
   6. How you verified the final code."

   Requested transparent documentation of AI-assisted development.

## 3. AI Output Accepted

The following AI-generated guidance was used or proposed for the project:

- Django model definitions for products, shipping boxes, orders, and order items.
- A box recommendation service based on product dimensions, total weight, box capacity, and packaging cost.
- A greedy three-dimensional packing heuristic that considers rectangular product rotations and non-overlapping placement.
- Django REST Framework endpoint guidance for retrieving box recommendations.
- An HTML dashboard structure for warehouse operations.
- CSS styling for a responsive dashboard.
- Vanilla JavaScript for calling the API and displaying recommendation results.
- Suggested automated tests for packing behavior and API responses.
- README documentation describing setup, project structure, features, API usage, limitations, and future improvements.

These outputs were treated as implementation guidance and require verification against the actual project.

## 4. Output Rejected or Modified

- React was not used because the selected frontend stack is HTML, CSS, and vanilla JavaScript.
- The greedy packing algorithm is not treated as a guaranteed optimal solver. Its limitations are documented, and stronger optimization may be required for production.
- The frontend communicates with the Django backend through an HTTP API instead of embedding recommendation logic in JavaScript.
- Documentation distinguishes implemented functionality from proposed future improvements.
- Any code that does not match the actual project structure, API response, or test results must be corrected before submission.

No other rejected AI output is claimed here; record additional changes if they occur during development.

## 5. Mistakes and Limitations Identified

The following issues were identified during review of the AI-generated implementation:

1. **Packing heuristic limitations:** A greedy placement algorithm may fail to find a valid arrangement even when one exists. A failed attempt is not proof that a box is unsuitable.

2. **Test coverage limitations:** Basic packing tests do not prove that all possible product arrangements are handled correctly.

3. **API response assumptions:** The JavaScript frontend depends on the response fields returned by Django. Changes to either side must be reflected in the other.

4. **Missing operational features:** The initial implementation does not automatically list pending orders or persist a confirmed packaging decision.

5. **Production considerations:** Authentication, authorization, input validation, protective packaging allowances, audit logs, and production deployment require further implementation and review.

6. **Verification status:** AI-generated code and documentation are not evidence that the application works. Actual results must be obtained by running the application and its tests.

## 6. How the Final Code Was Verified

The following verification steps are recommended. Mark them as completed only after running them successfully.

### Environment and configuration

- [ ] Confirmed Python and Django versions.
- [ ] Installed dependencies from `requirements.txt`.
- [ ] Ran database migrations successfully.
- [ ] Ran `python manage.py check` without errors.

### Backend and API

- [ ] Created products, shipping boxes, orders, and order items through Django Admin.
- [ ] Tested a product that fits within a box.
- [ ] Tested product rotation.
- [ ] Tested orders containing multiple products.
- [ ] Tested insufficient box weight capacity.
- [ ] Tested orders for which no suitable box was found.
- [ ] Verified that a nonexistent order returns HTTP 404.
- [ ] Confirmed that the API response matches the frontend's expected JSON structure.

### Frontend

- [ ] Opened the dashboard in a browser.
- [ ] Verified that CSS and JavaScript static files load correctly.
- [ ] Requested a recommendation for an existing order.
- [ ] Verified that the recommended box dimensions, weight, and cost display correctly.
- [ ] Tested invalid order IDs and API errors.
- [ ] Checked basic responsive behavior on a smaller screen.

### Automated tests

Run:

```bash
python manage.py check
python manage.py test packaging
```

**Actual verification results:** Fill in the Python/Django versions, test results, and any unresolved failures after executing these commands. Do not report tests as passing unless the terminal confirms success.

### Review and limitations

- Reviewed the packing algorithm's assumptions and limitations.
- Compared frontend field names with the actual API response.
- Distinguished implemented features from planned enhancements.
- Identified remaining work before production deployment.

## 7. Declaration

ChatGPT was used as an AI-assisted development tool for planning, implementation guidance, frontend development, testing suggestions, and documentation.

The AI-generated outputs are not independently verified merely because they were generated. The final implementation must be reviewed, executed, tested, and understood by the developer before submission or deployment.
