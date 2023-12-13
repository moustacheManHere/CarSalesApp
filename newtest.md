# Pytest

## API Tests:

- **User:**
  - Test add user
  - Test login API
- **Prediction:**
  - Test the prediction API

## Range Tests:

- **Prediction:**
  - Try inputting large values and negative values

## Consistency Tests:

- **Prediction:**
  - Input the same model with the same data multiple times and check consistency
- **API:**
  - Test if search results are consistent no matter how many times you request

## Expected Scenarios:

- **Prediction:**
  - Missing values for the ML model
- **Routes:**
  - Invalid request types like PUT and DELETE for routes
- **Forms:**
  - Try every form with missing data
- **Database:**
  - Init models with missing params

## Unexpected Scenarios:

- **User:**
  - Add a user
  - Login and obtain user ID
- **Prediction:**
  - Predict fixed input output
- **Database:**
  - Test initialization for each database class
  - Insert into the database and verify values
  - Remove from the database and ensure consistency
  - Edit the database and validate changes
  - Test populating cars DB
