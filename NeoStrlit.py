import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pymysql



dbconn = pymysql.connect(
    host='localhost',
    user='root',
    password='<password>',
    database='neodb'    
)

cur=dbconn.cursor()
cur.execute('use neodb')

with st.sidebar:
     with st.container(border=True):
         st.header('Navigation')
         options = ["Home","Queries", "Filters"]
         selection = st.pills('Options', options,default='Home',selection_mode="single")
if selection=="Home":
    st.title('_NASA Near Earth Objects_')
    st.divider()
    st.image("D:/DS ML&AI/31a0d1d5aacc178f5e75d38eaa5940a2.gif")
if selection=="Queries":
    st.title('_NASA Near Earth Objects_')
    st.divider()
    lis_options=['Count how many times each asteroid has approached Earth','Average velocity of each asteroid over multiple approaches','List top 10 fastest asteroids','Find potentially hazardous asteroids that have approached Earth more than 3 times','Find the month with the most asteroid approaches','Get the asteroid with the fastest ever approach speed','Sort asteroids by maximum estimated diameter','An asteroid whose closest approach is getting nearer over time','Display the name of each asteroid along with the date and miss distance of its closest approach to Earth','List names of asteroids that approached Earth with velocity > 50,000 km/h','Count how many approaches happened per month','Find asteroid with the highest brightness (lowest magnitude value)','Get number of hazardous vs non-hazardous asteroids','Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance','Find asteroids that came within 0.05 AU']
    QrySelc=st.selectbox('Choose your Query',lis_options,index=None,accept_new_options=False)
    st.divider()
    if QrySelc==lis_options[0]:
        sql0="select name ,count(*)  from asteroids group by name"
        cur.execute(sql0)
        res0=cur.fetchall()
        df=pd.DataFrame(res0,columns=['AsteroidName','No_of_Approaches'])
        st.dataframe(df)

    if QrySelc==lis_options[1]:
        sql1="select a.name ,avg(c.relative_velocity_kmph) from close_approach as c join asteroids as a on c.neo_reference_id=a.id group by a.name"
        cur.execute(sql1)
        res1=cur.fetchall()
        df=pd.DataFrame(res1,columns=['Name','Average Velocity'])
        st.dataframe(df)

    if QrySelc==lis_options[2]:
        sql2="select a.name,c.relative_velocity_kmph from close_approach as c join asteroids as a on c.neo_reference_id=a.id order by c.relative_velocity_kmph desc limit 10"
        cur.execute(sql2)
        res2=cur.fetchall()
        df=pd.DataFrame(res2,columns=['AsteroidName','Relative Velocity'])
        st.dataframe(df)

    if QrySelc==lis_options[3]:
        sql3="select a.name,count(*) as approaches from close_approach as c join asteroids as a on c.neo_reference_id=a.id where is_potentially_hazardous_asteroid=1 group by a.name having approaches>3"
        cur.execute(sql3)
        res3=cur.fetchall()
        df=pd.DataFrame(res3,columns=['AsteroidName','No_of_Approaches'])
        st.dataframe(df)


    if QrySelc==lis_options[4]:
        sql4="select monthname(close_approach_date) as ApproMonth,count(*) from close_approach group by ApproMonth"
        cur.execute(sql4)
        res4=cur.fetchall()
        df=pd.DataFrame(res4,columns=['Approach Month','No_of_Approaches'])
        st.dataframe(df)

    if QrySelc==lis_options[5]:
        sql5="select a.name,c.relative_velocity_kmph from close_approach  as c join asteroids as a on c.neo_reference_id=a.id order by c.relative_velocity_kmph desc limit 1"
        cur.execute(sql5)
        res5=cur.fetchall()
        df=pd.DataFrame(res5,columns=['Name','Approach Speed'])
        st.dataframe(df)

    if QrySelc==lis_options[6]:
        sql6="select name,estimated_diameter_max_km from asteroids order by estimated_diameter_max_km desc"
        cur.execute(sql6)
        res6=cur.fetchall()
        df=pd.DataFrame(res6,columns=['Name','Max Diameter'])
        st.dataframe(df)


    if QrySelc==lis_options[7]:
        sql7="select a.name from close_approach as c join asteroids as a on c.neo_reference_id=a.id order by c.close_approach_date asc,c.miss_distance_lunar desc limit 1"
        cur.execute(sql7)
        res7=cur.fetchall()
        df=pd.DataFrame(res7,columns=['Name'])
        st.dataframe(df)

    if QrySelc==lis_options[8]:
        sql8="with cte as (select a.name as name,c.close_approach_date as approachDate,c.miss_distance_km as distance,row_number() over (partition by a.name,c.close_approach_date order by c.miss_distance_km asc)as rnk from close_approach as c join asteroids as a on c.neo_reference_id=a.id) select name,approachDate,distance from cte where rnk=1"
        cur.execute(sql8)
        res8=cur.fetchall()
        df=pd.DataFrame(res8,columns=['Name','Approach Date','Miss Distance'])
        st.dataframe(df)

    if QrySelc==lis_options[9]:
        sql9="select a.name from close_approach as c join asteroids as a on c.neo_reference_id=a.id where relative_velocity_kmph>50000"
        cur.execute(sql9)
        res9=cur.fetchall()
        df=pd.DataFrame(res9,columns=['Name'])
        st.dataframe(df)

    if QrySelc==lis_options[10]:
        sql10="select monthname(close_approach_date),count(*) from close_approach group by close_approach_date"
        cur.execute(sql10)
        res10=cur.fetchall()
        df=pd.DataFrame(res10,columns=['Month','Approaches'])
        st.dataframe(df)

    if QrySelc==lis_options[11]:
        sql11="select name from asteroids where absolute_magnitude_h in(select min(absolute_magnitude_h) from asteroids )"
        cur.execute(sql11)
        res11=cur.fetchall()
        df=pd.DataFrame(res11,columns=['Name'])
        st.dataframe(df)

    if QrySelc==lis_options[12]:
        sql12="select distinct is_potentially_hazardous_asteroid ,count(*) from asteroids group by is_potentially_hazardous_asteroid;"
        cur.execute(sql12)
        res12=cur.fetchall()
        df=pd.DataFrame(res12,columns=['Status','Count'])
        st.dataframe(df)

    if QrySelc==lis_options[13]:
        sql13="select a.name,c.close_approach_date,c.miss_distance_lunar from close_approach as c join asteroids as a on c.neo_reference_id=a.id where miss_distance_lunar<1"
        cur.execute(sql13)
        res13=cur.fetchall()
        df=pd.DataFrame(res13,columns=['Name','Approach Date','Lunar Distance'])
        st.dataframe(df)

    if QrySelc==lis_options[14]:
        sql14="select a.name from close_approach as c join asteroids as a on c.neo_reference_id=a.id where `astronomical(AU)`<0.05"
        cur.execute(sql14)
        res14=cur.fetchall()
        df=pd.DataFrame(res14,columns=['Name'])
        st.dataframe(df)
        
        
    

if selection=="Filters":
    st.title('_NASA Near Earth Objects_')
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        rv=st.slider('Relative Velocity',min_value=500,max_value=200000)
        minD=st.slider('Min Estimated Diameter',min_value=0.00001,max_value=6.0)
        maxD=st.slider('Max Estimated Diameter',min_value=0.0001,max_value=12.0)
    with col2:
        ld=st.slider('Lunar Distance',min_value=0.001,max_value=200.0)
        au=st.slider('Astronomical Units',min_value=0.0000001,max_value=1.0)
        hs=st.selectbox('Hazardous state',['1','0'])
    with col3:
        sd=st.date_input('Start Date',datetime.date(2024, 1, 1))
        ed=st.date_input('End Date',datetime.date(2025, 5, 31))
    st.divider()
    butt=st.button('Apply Filters')
    st.divider()
    if butt:
        selQry=f"select * from asteroids as a join close_approach as c on c.neo_reference_id=a.id where c.relative_velocity_kmph<{rv} and a.estimated_diameter_min_km<{minD} and a.estimated_diameter_max_km<{maxD} and c.miss_distance_lunar<{ld} and c.`astronomical(AU)`<{au} and a.is_potentially_hazardous_asteroid={hs} "
        cur.execute(selQry)
        res=cur.fetchall()
        df=pd.DataFrame(res,columns=['ID','Name','Magnitude','Min Diameter','Max Diameter','Is Hazardous','Neo Reference ID','Approach Date','Relative Velocity','Astronomical Unit','Miss distance','Lunar Distance','Orbiting Body'])
        st.dataframe(df)
        st.divider()


