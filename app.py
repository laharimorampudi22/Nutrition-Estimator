echo from flask import Flask, render_template, request, jsonify>app.py
echo import json, re>>app.py
echo app=Flask(__name__)>>app.py
echo NUTRITION_DATA=json.load(open('model/nutrition_data.json'))>>app.py
echo def estimate_nutrition(txt):>>app.py
echo.    total={'calories':0,'protein':0,'fat':0,'carbs':0}>>app.py
echo.    for ing in [i.strip() for i in txt.split(',')]:>>app.py
echo.        m=re.search(r'([0-9.]+)\s*(cup|tbsp|g|gram|grams)?\s*(.*)',ing)>>app.py
echo.        if not m:continue>>app.py
echo.        q=float(m.group(1));u=m.group(2) or 'unit';n=m.group(3).lower()>>app.py
echo.        for k,v in NUTRITION_DATA.items():>>app.py
echo.            if k in n:>>app.py
echo.                s=q>>app.py
echo.                if 'cup' in u:s*=v.get('g_per_cup',100)/100>>app.py
echo.                elif 'tbsp' in u:s*=v.get('g_per_tbsp',15)/100>>app.py
echo.                elif 'g' in u:s*=1/100>>app.py
echo.                [total.__setitem__(x,total[x]+v[x]*s) for x in total]>>app.py
echo.    return{t:round(v,2) for t,v in total.items()}>>app.py
echo @app.route('/')>>app.py
echo def home():return render_template('index.html')>>app.py
echo @app.route('/estimate',methods=['POST'])>>app.py
echo def est():return jsonify(estimate_nutrition(request.form['ingredients']))>>app.py
echo if __name__=='__main__':app.run(debug=True)>>app.py
