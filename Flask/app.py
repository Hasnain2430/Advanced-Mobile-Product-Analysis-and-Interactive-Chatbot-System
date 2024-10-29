from flask import Flask, render_template, request
import pandas as pd
import re
from nltk.tokenize import word_tokenize

app = Flask(__name__)
Mobile_Data = pd.read_csv("Final_Phone_Data.csv", index_col='Unnamed: 0')
review_data = pd.read_csv("Final_Review_Data.csv",index_col='Unnamed: 0')
Mobile_Data['Price'] = pd.to_numeric(Mobile_Data['Price'].str.replace("Rs","").str.replace(".","").str.replace(",",""))
Mobile_Data['Company'] = Mobile_Data['Company'].str.lower() 
Mobile_Data['Product Name'] = Mobile_Data['Product Name'].str.lower() 
Mobile_Data['Specifications'] = Mobile_Data['Specifications'].str.lower() 
Mobile_Data['Rating'] = pd.to_numeric(Mobile_Data['Rating'].str.replace('-','0'))
Mobile_Data['Total Ratings'] = pd.to_numeric(Mobile_Data['Total Ratings'].str.replace('No','0'))
Mobile_Data['Total Questions Answered'] = pd.to_numeric(Mobile_Data['Total Questions Answered'].str.replace('-','0'))

def clean_string(input_string):
    clean_string = re.sub(r'(?<!\d)[^\w\s.](?!\d)', '', input_string)
    clean_string = clean_string.lower()
    # print(clean_string)
    words = word_tokenize(clean_string)
    return words

def clean_string2(input_string):
    clean_string = re.sub(r'(?<!\d)[^\w\s.](?!\d)', '', input_string)
    clean_string = clean_string.lower()
    # print(clean_string)
    # words = word_tokenize(clean_string)
    return clean_string

def contains_Brand(text):
    Brands = ['redmi','apple','infinix','samsung','tecno','xiaomi','vivo','realme','itel','sparx','vgotel','nokia','oppo','combo','zte','imported','y81','vgo','iphone','lg','honor']
    brands = []
    cond = False
    for word in text:
        if word in Brands:
            brands.append(word)
            cond = True
    return cond,brands

def contains_Rating(text):
    words = ['score','ranking','rating','rated']
    for word in text:
        if word in words:
            return True

def to_digit(value):
    digits =re.compile(r'\d+').findall(value)
    digits = [int(d) for d in digits]
    value = digits[0]*1000    
    return value


def contains_digit(text):
    num = []
    num2 = []
    for word in text:
        if 'k' in word:
            numm = to_digit(word)
            num.append(numm)
        try:
            if (word.isdigit()):
                num.append(int(word))
            else:
                num2.append(float(word))
        except ValueError:
            pass
    return num,num2

def contains_highest(text):
    dict = ['highest','greater','more','higher','high','top','good','above','best','more than']
    for word in text:
        if word in dict:
            return True
            
def contains_lowest(text):
    dict = ['lower','lowest','less','lesser','under','below','worse','low','worst']
    for word in text:
        if word in dict:
            return True

def contains_price_low(text):
    dict = ['under','below','lower','lesser']
    for word in text:
        if word in dict:
            return True


def contains_price_high(text):
    dict = ['greater','greater than','above']
    for word in text:
        if word in dict:
            return True
                        
def Display_Brands(query):
    bool,brand = contains_Brand(query) # Brand Given or Not
    num6,num7 = contains_digit(query)
    if (bool==True):
        if (len(brand)==1):
            brand = brand[0]
            if (contains_Rating(query)):          # Contains Rating?
                num,num2 = contains_digit(query)       # Checking if Rating specified or not
                if(len(num2)==1 and len(num)==0):                  # only rating given
                    rating = num2[0]
                    if (contains_highest(query)):    # Rating Higher?
                        query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']>rating)]
                        query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        print("Working")
                        query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']<rating)]
                        query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                        return query
                    
                elif(len(num2)==1 and len(num)==1):     # Rating and Price Given
                    price = num[0]
                    rating = num2[0]
                    if (contains_highest(query)):   # Rating Higher?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']>rating) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']>rating) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                            return query
                    elif (contains_lowest(query)):  # Rating Lower?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']<rating) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']<rating) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                            return query
                    
                
                elif(len(num)==2 and len(num2)==1):   # Rating + Price in between
                    
                    price1 = num[0]
                    price2 = num[1]
                    rating = num2[0]

                    if (contains_highest(query)):   # Rating Higher?
                        query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']>rating) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & (Mobile_Data['Rating']<rating) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                        return query
                        
                elif (len(num)==1 and len(num2)==0):
                    price = num[0]
                    if (contains_highest(query)):   # Rating Higher?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                    elif (contains_lowest(query)):  # Rating Lower?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                            
                elif (len(num)==2 and len(num2)==0):
                    price1 = num[0]
                    price2 = num[1]

                    if (contains_highest(query)):   # Rating Higher?
                        query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        query = Mobile_Data[(Mobile_Data['Company'].str.contains(brand)) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    
                    
                else:    # Rating is not specified
                    
                    if (contains_highest(query)):  # High Rated Product?
                        query = Mobile_Data[Mobile_Data['Company'].str.contains(brand)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Low Rated Product?
                        query = Mobile_Data[Mobile_Data['Company'].str.contains(brand)]
                        query = query.sort_values(by='Rating', ascending=True)
                        return query    
                        
            elif (len(num6)>0):
                print(len(contains_digit(query)))
                num,num2 = contains_digit(query)
                if (len(num)==1):
                    price = num[0]
                    if (contains_highest(query)):  # High Rated Product?
                        print("Highest")
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand))) & (Mobile_Data['Price']>price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Low Rated Product?
                        print("Lowest")
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand))) & (Mobile_Data['Price']<price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                elif (len(num)==2):
                    price1 = num[0]
                    price2 = num[1]
                    query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand))) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                    query = query.sort_values(by='Price', ascending=False)
                    return query
            else:
                if(contains_lowest(query)):
                    query = Mobile_Data[Mobile_Data['Company'].str.contains(brand)]
                    query = query.sort_values(by=['Rating','Total Ratings'], ascending=True)
                    return query
                else:
                    query = Mobile_Data[Mobile_Data['Company'].str.contains(brand)]
                    query = query.sort_values(by=['Rating', 'Total Ratings'], ascending=False)
                    return query
            
        elif(len(brand)==2):
            
            brand1 = brand[0]
            brand2 = brand[1] 
            if (contains_Rating(query)):          # Contains Rating?
                num,num2 = contains_digit(query)       # Checking if Rating specified or not
                if(len(num2)==1 and len(num)==0):                  # only rating given
                    rating = num2[0]
                    if (contains_highest(query)):    # Rating Higher?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']>rating)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']<rating)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    
                elif(len(num2)==1 and len(num)==1):     # Rating and Price Given
                    price = num[0]
                    rating = num2[0]
                    if (contains_highest(query)):   # Rating Higher?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']>rating) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']>rating) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                    elif (contains_lowest(query)):  # Rating Lower?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']<rating) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']<rating) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                
                elif(len(num)==2 and len(num2)==1):   # Rating + Price in between
                    
                    price1 = num[0]
                    price2 = num[1]
                    rating = num2[0]

                    if (contains_highest(query)):   # Rating Higher?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']>rating) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Price', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Rating']<rating) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Price', ascending=False)
                        return query
                        
                elif (len(num)==1 and len(num2)==0):
                    price = num[0]
                    if (contains_highest(query)):   # Rating Higher?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                    elif (contains_lowest(query)):  # Rating Lower?
                        cond = contains_price_low(query)
                        cond2 = contains_price_high(query)
                        if (cond==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) &  (Mobile_Data['Price']<price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                        elif (cond2==True):
                            query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) &  (Mobile_Data['Price']>price)]
                            query = query.sort_values(by='Rating', ascending=False)
                            return query
                            
                elif (len(num)==2 and len(num2)==0):
                    price1 = num[0]
                    price2 = num[1]

                    if (contains_highest(query)):   # Rating Higher?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    
                    
                else:    # Rating is not specified
                    
                    if (contains_highest(query)):  # High Rated Product?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2)))]
                        query = query.sort_values(by='Rating', ascending=False).head(5)
                        return query
                    elif (contains_lowest(query)):   # Low Rated Product?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2)))]
                        query = query.sort_values(by='Rating', ascending=True).head(5)
                        return query    
                        
            elif (len(num6)>0):
                num,num2 = contains_digit(query)
                if (len(num)==1):
                    price = num[0]
                    if (contains_highest(query)):  # High Rated Product?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Price']>price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Low Rated Product?
                        query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & (Mobile_Data['Price']<price)]
                        query = query.sort_values(by='Rating', ascending=True)
                        return query
                elif (len(num)==2):
                    price1 = num[0]
                    price2 = num[1]
                    query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2))) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                    query = query.sort_values(by='Price', ascending=False)
                    return query
            else:
                query = Mobile_Data[((Mobile_Data['Company'].str.contains(brand1)) | (Mobile_Data['Company'].str.contains(brand2)))]
                query = query.sort_values(by='Rating', ascending=False)
                return query
    else:
        num1,num2 = contains_digit(query)
        if (contains_Rating(query)):
            if(len(num1)==0 and len(num2)==1): # only rating given
                rating = num2[0]
                if (contains_highest(query)):    # Rating Higher?
                    query = Mobile_Data[(Mobile_Data['Rating']>rating)]
                    query = query.sort_values(by='Rating', ascending=False)
                    return query
                elif (contains_lowest(query)):   # Rating Lower?
                    query = Mobile_Data[(Mobile_Data['Rating']<rating)]
                    query = query.sort_values(by='Rating', ascending=False)
                    return query
                    
            elif(len(num1)==1 and len(num2)==1):
                price = num1[0]
                rating = num2[0]
                if (contains_highest(query)):   # Rating Higher?
                    cond = contains_price_low(query)
                    cond2 = contains_price_high(query)
                    if (cond==True):
                        query = Mobile_Data[(Mobile_Data['Rating']>rating) &  (Mobile_Data['Price']<price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (cond2==True):
                        query = Mobile_Data[(Mobile_Data['Rating']>rating) &  (Mobile_Data['Price']>price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                elif (contains_lowest(query)):  # Rating Lower?
                    cond = contains_price_low(query)
                    cond2 = contains_price_high(query)
                    if (cond==True):
                        query = Mobile_Data[(Mobile_Data['Rating']<rating) &  (Mobile_Data['Price']<price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                    elif (cond2==True):
                        query = Mobile_Data[(Mobile_Data['Rating']<rating) &  (Mobile_Data['Price']>price)]
                        query = query.sort_values(by='Rating', ascending=False)
                        return query
                        
            elif(len(num1)==2 and len(num2)==1):   # Rating + Price in between
                    
                    price1 = num1[0]
                    price2 = num1[1]
                    rating = num2[0]

                    if (contains_highest(query)):   # Rating Higher?
                        query = Mobile_Data[(Mobile_Data['Rating']>rating) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Price', ascending=False)
                        return query
                    elif (contains_lowest(query)):   # Rating Lower?
                        query = Mobile_Data[(Mobile_Data['Rating']<rating) & ((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                        query = query.sort_values(by='Price', ascending=False)
                        return query
                        
            elif(len(num1)==1 and len(num2)==0):
                price = num1[0]
                print(price)
                if (contains_price_high(query)):  # High Rated Product?
                    query = Mobile_Data[(Mobile_Data['Price']>price)]
                    query = query.sort_values(by=['Rating', 'Total Ratings'], ascending=[False, False])
                    return query
                elif (contains_price_low(query)):   # Low Rated Product?
                    query = Mobile_Data[(Mobile_Data['Price']<price)]
                    query = query.sort_values(by=['Rating', 'Total Ratings'], ascending=[False, False])
                    return query
                    
        elif (len(num1)>0):
            if (len(num1)==1):
                price = num1[0]
                if (contains_price_high(query)):  # High Rated Product?
                    query = Mobile_Data[(Mobile_Data['Price']>price)]
                    query = query.sort_values(by=['Rating', 'Total Ratings'], ascending=[False, False])
                    return query
                elif (contains_price_low(query)):   # Low Rated Product?
                    query = Mobile_Data[(Mobile_Data['Price']<price)]
                    query = query.sort_values(by=['Rating', 'Total Ratings'], ascending=[False, False])
                    return query
            elif (len(num1)==2):
                price1 = num1[0]
                price2 = num1[1]
                query = Mobile_Data[((Mobile_Data['Price']>price1) & (Mobile_Data['Price']<price2))]
                query = query.sort_values(by=['Rating','Total Ratings'], ascending=False)
                return query  
        else:   
            if (contains_highest(query)):  # High Rated Product?
                query = Mobile_Data.sort_values(by=['Rating', 'Total Ratings'], ascending=False).head(5)
                return query
            elif (contains_lowest(query)):   # Low Rated Product?
                query = Mobile_Data.sort_values(by=['Rating', 'Total Ratings'], ascending=True).head(5)
                return query 

def query_processor(query):
    query = clean_string(query)
    query = Display_Brands(query)
    return query

def query_processor2(query):
    query1 = clean_string2(query)
    query1 = Mobile_Data[(Mobile_Data['Product Name'].str.contains(query))]
    query1 = query1.sort_values(by='Rating', ascending=False)
    if(len(query1)==0):
        query = query_processor(query)
        return query
    else:
        
        return query1       



def search_reviews(product_id):
    unique_product_ids = data['Product ID']
    filtered_reviews = review_data[review_data['Product ID'].isin(unique_product_ids)]
    filtered_reviews = filtered_reviews[filtered_reviews['Product ID'] == product_id]
    return filtered_reviews

@app.route('/search_reviews', methods=['POST'])
def search_reviews_route():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        filtered_reviews = search_reviews(product_id)
        return render_template('reviews.html', reviews=filtered_reviews.to_dict('records'))

                        

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         query = request.form['query']  
#         filtered_data =  query_processor2(query)
#         filtered_data = filtered_data.head()
#         return render_template('home.html', data=filtered_data.to_dict('records'), query=query)
#     return render_template('home.html', data=None, query=None)


# @app.route('/additional_search', methods=['POST'])
# def additional_search():
#     query = request.form['additional-query']
#     filtered_data = reviews(query)
#     return render_template('home.html', data=None, additional_data=filtered_data.to_dict('records'))

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html', data=Mobile_Data.to_dict('records'))




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        additional_query = request.form.get('additional-query')  # Get the value from the additional search bar
        if additional_query:  # If the additional query is not empty
            filtered_additional_data = search_reviews(additional_query)
            return render_template('home.html', data=None, additional_data=filtered_additional_data.to_dict('records'), query=query)
        else:
            query = request.form['query']
            filtered_data = query_processor2(query)
            filtered_data = filtered_data.head()
            return render_template('home.html', data=filtered_data.to_dict('records'), query=query)
    return render_template('home.html', data=None, query=None)

@app.route('/additional_search', methods=['POST'])
def additional_search():
    query = request.form['additional-query']
    filtered_data = search_reviews(query)
    return render_template('home.html', data=None, additional_data=filtered_data.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)