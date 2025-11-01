# Project - Expense Tracker 💸📊

#### This application helps you track your expenses.

## Features:
- Add, view, edit and delete expenses.
- Category-wise summaries, analytics-charts.


## Folder Structure of the project

```
personal_expense_tracker/
│
├── streamlit_app/                 
│   ├── app.py                      
│   │── add_expense.py             
│   │── view_expenses.py 
│   └── delete_expense.py    
│   └── edit_expense.py       
│   │── analytics.py               
│   │── utils.py                   
│
├── lambda_functions/               # (Codes should be tested in the AWS lambda consoles)  
│   ├── lambda_functions.py                
│   ├── db_operations.py           
│   ├── s3_backup.py               
│   └── utils.py                              
│
├── .env                    
├── .gitignore                     
├── requirements.txt               
├── README.md                      
└── venv/                          

```

### .env format

```
API_URL=
DYNAMODB_TABLE=
S3_BUCKET=
```

## Featured Demonstrations

#### User Interface (Add Expenses)

<img width="1920" height="1128" alt="add expense" src="https://github.com/user-attachments/assets/c62d4b52-8f44-443f-aa9e-00417bf2d78d" />

#### User Interface (View Expenses)



#### User Interface (Analytics)

<img width="1920" height="1128" alt="analytics" src="https://github.com/user-attachments/assets/e74b8347-db96-40ee-95f4-b9dfae6ed2ef" />

#### DynamoDB table

<img width="1920" height="1128" alt="DynamoDB table" src="https://github.com/user-attachments/assets/9298e3ac-0b43-4af8-9626-d66aea441142" />

#### API Gateways

<img width="1920" height="1128" alt="API gateways" src="https://github.com/user-attachments/assets/e6fcbca3-bf6f-499a-9743-5a5ea459443c" />

#### Lambda Functions

<img width="1920" height="1128" alt="lambda function" src="https://github.com/user-attachments/assets/18c9379c-3e1c-4093-9ad9-d239df2c971b" />

#### S3 Bucket

<img width="1920" height="1128" alt="s3 buckets" src="https://github.com/user-attachments/assets/961db78c-dcb5-4264-b5a0-6e541af4cb27" />

#### Eventbridge

<img width="1920" height="1128" alt="Eventbridge" src="https://github.com/user-attachments/assets/4664758b-83df-413e-8ae3-fdb245679bd0" />


#### ------ END ------
