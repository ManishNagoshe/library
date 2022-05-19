API: Post

<https://library-manish-nagoshe.herokuapp.com/signup>

**Description**: Used to sign up by the user

|<p>**Fields required for API:**</p><p>{</p><p>`  `"email": "string",</p><p>`  `"name": "string",</p><p>`  `"password": "string",</p><p>`  `"role": 0</p><p>}</p><p></p>|<p>**Description of the fields:**</p><p>**email:** A email address of the user</p><p>**name:** Full name of the user</p><p>**password:** password to use login must be of 8-character length</p><p>Role: 1 or 2 (1 Librarian, 2 Member)</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|{“msg”:”Name is not valid”}|Name field is blank or to short to be considered as name|
|{“Password is length is shorter than 8”}|Password is too short|
|{“Email not valid”}|User has not entered email correctly|
|{“error occurred, role is invalid or user may exist”}|Role is not 1 or 2 or user may exist or connection error with database|


**Success Msg:** {“msg”:”user created successfully”}

API: Post

<https://library-manish-nagoshe.herokuapp.com/login>

**Description**: Used to login by the user

|<p>**Fields required for API:**</p><p>{</p><p>`  `"email": "string",</p><p>`  `"password": "string"</p><p>}</p><p></p>|<p>**Description of the fields:**</p><p>**email:** A email address of the user</p><p>**password:** password to use login</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|{"msg":"Connection error"}|connection error with database|
|{"msg": "invalid credentials"}|Password or email is not correct|


**Success Msg:** {"msg":"login Successful"}

API: Get

<https://library-manish-nagoshe.herokuapp.com/getrole> 

**Description**: Used to get the role of the user

|<p>**Fields required for API:**</p><p></p>|<p>**Description of the fields:**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|


**Success Msg:** 1 or 2

API: Get

<https://library-manish-nagoshe.herokuapp.com/getusername>  

**Description**: Used to get the name of the user

|<p>**Fields required for API:**</p><p></p>|<p>**Description of the fields:**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|


**Success Msg:** Name of the user for e.g. Manish Nagoshe

API: Put

<https://library-manish-nagoshe.herokuapp.com/logout>  

**Description**: Used to logout

|<p>**Fields required for API:**</p><p></p>|<p>**Description of the fields:**</p><p></p>|
| :- | :- |

**Success Msg:** {"msg":"logout successful"}


API: Post

<https://library-manish-nagoshe.herokuapp.com/changepassword>  

**Description**: Used to change the password of the user

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"old\_password": "string",**</p><p>`  `**"new\_password": "string"**</p><p>**}**</p><p></p>|<p>**Description of the fields:**</p><p>**old\_password: old or earlier password used for login,**</p><p>**new\_password: New password to be used from now onwards**</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"error":"Password not updated, check old password"}|Old password provided is not correct|


**Success Msg:** {"msg":"password changed successfully"}

API: Post

<https://library-manish-nagoshe.herokuapp.com/get_user_details>  

**Description**: Used to get the user details for role 1 (Librarian) only

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"startindex": 0,**</p><p>`  `**"endindex": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: it is number from which record has to fetched**</p><p>**endindex: it is the number upto record to be fetched**</p><p>**e.g**</p><p>**startindex: 0 and endindex:10 will give you record from 1 to 10**</p><p>**startindex: 10 and endindex:20 will give you record from 11 to 20**</p><p>Maximum 10 record can be fetched at one time for pagination</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|


**Success Msg:** Json array of user details

[

`  `{

`    `"id": 1,

`    `"email": "manish@gmail.com",

`    `"name": "Manish",

`    `"status": "Active",

`    `"role": 1

`  `},

`  `{

`    `"id": 2,

`    `"email": "tushar@gmail.com",

`    `"name": "Tushar Nagoshe",

`    `"status": "Active",

`    `"role": 2

`  `}

]



API: Post

<https://library-manish-nagoshe.herokuapp.com/get_user_details_by_id> 

**Description**: Used to get the user details by id of the user for role 1 (Librarian) only

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"id": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>Id: user id</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|


**Success Msg:** Json response

{

`  `"id": 2,

`  `"email": "tushar@gmail.com",

`  `"name": "Tushar Nagoshe",

`  `"status": "Active",

`  `"role": 2

}

API: Put

<https://library-manish-nagoshe.herokuapp.com/modify_user_details_by_id>

**Description**: Used to change the name of the user by user id for role 1 (Librarian) only

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"name": "string",**</p><p>`  `**"id": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>name: modified user name </p><p>id: user id of which name has to be changed</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|


**Success Msg:** {"msg":"Data updated"}

API: Put

<https://library-manish-nagoshe.herokuapp.com/disable_account>

**Description**: Used to disable the own account 

|<p>**Fields required for API:**</p><p></p>|<p>**Description of the fields:**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|


**Success Msg:** {"msg":"Your account is disabled"}

API: Post

<https://library-manish-nagoshe.herokuapp.com/book/insertbook> 

**Description**: Used to add the new book for the role 1 only

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"title": "string",**</p><p>`  `**"author": "string",**</p><p>`  `**"price": 0**</p><p>**}**</p><p></p>|<p>**Description of the fields:**</p><p>**title: title of the book**</p><p>**author: Authors of the book**</p><p>**price: Price of the book in float value**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Name is not valid"}|Title of the book is empty|
|{"msg":"Author is short in length"}|Author field is empty|
|{"msg":"invalid price"}|Price cannot be negative|
|{"msg":"error occurred while registering the book please check all fields or may connection error"}|Connection error of may be field value error|
` `Accno: Accession number of the book

**Success Msg:** {"msg":"Book registered successfully","accno":number}

API: Post

<https://library-manish-nagoshe.herokuapp.com/book/getallbooks_with_start_end_index>  

**Description**: used to get details of all the book order by id

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"startindex": 0,**</p><p>`  `**"endindex": 10**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: it is number from which record has to fetched**</p><p>**endindex: it is the number upto record to be fetched**</p><p>**e.g**</p><p>**startindex: 0 and endindex:10 will give you record from 1 to 10**</p><p>**startindex: 10 and endindex:20 will give you record from 11 to 20**</p><p>Maximum 10 record can be fetched at one time for pagination</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** Json array containing books details

[

`  `{

`    `"accno": 5,

`    `"title": "Python",

`    `"authors": "Dev",

`    `"price": 100,

`    `"status": "Available"

`  `},

`  `{

`    `"accno": 6,

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"price": 200,

`    `"status": "Available"

`  `}

]



API: Post

<https://library-manish-nagoshe.herokuapp.com/book/searchbook>  

**Description**: used to search the book by title and / or authors

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"title": “string”,**</p><p>`  `**"authors": “string”,**</p><p>`  `**"startindex": 0,**</p><p>`  `**"endindex": 10**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: it is number from which record has to fetched**</p><p>**endindex: it is the number upto record to be fetched**</p><p>**e.g**</p><p>**startindex: 0 and endindex:10 will give you record from 1 to 10**</p><p>**startindex: 10 and endindex:20 will give you record from 11 to 20**</p><p>Maximum 10 record can be fetched at one time for pagination</p><p>**title:** few character/ words from title of the book. If provided “null” it will select all title</p><p>**authors:** few character/ words from authors of the book. If provided “null” it will select all authors</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** Json array containing books details

[

`  `{

`    `"accno": 5,

`    `"title": "Python",

`    `"authors": "Dev",

`    `"price": 100,

`    `"status": "Available"

`  `},

`  `{

`    `"accno": 6,

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"price": 200,

`    `"status": "Available"

`  `}

]

API: Post

<https://library-manish-nagoshe.herokuapp.com/book/issuebook> 

**Description**: used to issue the book for role 1 only

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"accno": 0,**</p><p>`  `**"userid": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**accno: Accession number of the book**</p><p>**userid": user id**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Book is not available"}|Book is not available to issue, it may already issued or deleted or invalid accno number|
` `Accno: Accession number of the book

**Success Msg:** {"msg":"Book issued successfully"}


API: Put

<https://library-manish-nagoshe.herokuapp.com/book/delete_book> 

**Description**: used to delete the book for role 1 only (book records still remains)

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"accno": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**accno: Accession number of the book**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Book is already deleted or not available"}|Book is already deleted or invalid accno number|
` `Accno: Accession number of the book

**Success Msg:** {"msg":"Book Deleted successfully"}

API: Put

<https://library-manish-nagoshe.herokuapp.com/book/update_book> 

**Description**: used to update the book for role 1 only 

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"accno": 0,**</p><p>`  `**"title": "string",**</p><p>`  `**"author": "string",**</p><p>`  `**"price": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**accno: Accession number of the book who’s details need to be changed**</p><p>**title: Title of the book**</p><p>**author: authors of the book**</p><p>**price: price of the book**</p><p></p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Book is already deleted or not available"}|Book is already deleted or invalid accno number|
` `Accno: Accession number of the book

**Success Msg:** {"msg":"Book updated successfully"}

API: Put

<https://library-manish-nagoshe.herokuapp.com/book/returnbook> 

**Description**: used to return the book for role 1 only 

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"accno": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**accno: Accession number of the book who’s details need to be changed**</p><p></p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Book is not Issued"}|Book is not issued to anyone|
|{"msg":"Please check accno"}|Accno number is not correct|
` `Accno: Accession number of the book

**Success Msg:** {"msg":"Book Returned successfully"}


API: Post

<https://library-manish-nagoshe.herokuapp.com/report/user_report>  

**Description**: used to get book card of the user for role 1 only 

|<p>**Fields required for API:**</p><p>**{**</p><p>`  `**"id": 0,**</p><p>`  `**"startindex": 0,**</p><p>`  `**"endindex": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**id: user id**</p><p>**startindex: startindex**</p><p>**endindex: endindex**</p><p>**refer earlier api**</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** json array

[

`  `{

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"issuedate": "2022-05-18",

`    `"returndate": "2022-05-18"

`  `},

`  `{

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"issuedate": "2022-05-18",

`    `"returndate": "2022-05-18"

`  `},

`  `{

`    `"title": "Python",

`    `"authors": "Dev",

`    `"issuedate": "2022-05-18",

`    `"returndate": "2022-05-18"

`  `},

`  `{

`    `"title": "C#",

`    `"authors": "troy",

`    `"issuedate": "2022-05-19",

`    `"returndate": null

`  `}

]

API: Post

<https://library-manish-nagoshe.herokuapp.com/report/personal_report>  

**Description**: used to get own book card

|<p>**Fields required for API:**</p><p>**{**</p><p>`    `**"startindex": 0,**</p><p>`  `**"endindex": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: startindex**</p><p>**endindex: endindex**</p><p>**refer earlier api**</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** json array

[

`  `{

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"issuedate": "2022-05-18",

`    `"returndate": "2022-05-18"

`  `},

`  `{

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"issuedate": "2022-05-18",

`    `"returndate": "2022-05-18"

`  `},

`  `{

`    `"title": "Python",

`    `"authors": "Dev",

`    `"issuedate": "2022-05-18",

`    `"returndate": "2022-05-18"

`  `},

`  `{

`    `"title": "C#",

`    `"authors": "troy",

`    `"issuedate": "2022-05-19",

`    `"returndate": null

`  `}

]

API: Post

<https://library-manish-nagoshe.herokuapp.com/report/Book_Usage_report> 

**Description**: used to report of the particular title of the book  usage for role 1 only 

|<p>**Fields required for API:**</p><p>**{**</p><p>`   `**"startindex": 0,**</p><p>`  `**"endindex": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: startindex**</p><p>**endindex: endindex**</p><p>**refer earlier api**</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** json array (count indicates how many times a title has issued)

[

`  `{

`    `"title": "C#",

`    `"authors": "troy",

`    `"count": 1

`  `},

`  `{

`    `"title": "Fastapi",

`    `"authors": "Tud",

`    `"count": 2

`  `},

`  `{

`    `"title": "Python",

`    `"authors": "Dev",

`    `"count": 1

`  `}

]





API: Post

<https://library-manish-nagoshe.herokuapp.com/report/Book_Usage_report_pdf>

**Description**: used to PDF report of the particular title of the book  usage for role 1 only 

|<p>**Fields required for API:**</p><p>**{**</p><p>`   `**"startindex": 0,**</p><p>`  `**"endindex": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: startindex**</p><p>**endindex: endindex**</p><p>**refer earlier api**</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** pdf file

![](images/technical\_doc1.002.png)


API: Post

<https://library-manish-nagoshe.herokuapp.com/report/Book_Usage_report_xlsx> 

**Description**: used to xlsx report of the particular title of the book  usage for role 1 only 

|<p>**Fields required for API:**</p><p>**{**</p><p>`   `**"startindex": 0,**</p><p>`  `**"endindex": 0**</p><p>**}**</p>|<p>**Description of the fields:**</p><p>**startindex: startindex**</p><p>**endindex: endindex**</p><p>**refer earlier api**</p>|
| :- | :- |

**Possible Errors Msg:**

|**Error**|**Description**|
| :- | :- |
|<p>HTTP\_404\_NOT\_FOUND,</p><p>` `Msg:Login Expired</p>|Login has expired|
|<p>HTTP\_404\_NOT\_FOUND,</p><p>invalid user</p>|User has not logged in or not a valid user|
|{"msg":"Connection error"}|connection error with database|
|{"msg":"Maximum 10 books can be fetched"}|The difference between startindex and endindex is more than 10|
|{"msg":"Start index minimum value should be zero"}|Startindex cannot be negative|
|{"msg":"end index should be greater than start index"}|Endindex should be larger than startindex|
` `Accno: Accession number of the book

**Success Msg:** xlsx file

![](images/technical\_doc1.003.png)

