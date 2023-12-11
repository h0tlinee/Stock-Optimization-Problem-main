from Cell import *
from Optimizator import *
from Queue import *
from Stock import *
from flask import Flask, render_template, request, flash, redirect, url_for,json,jsonify
from input_handler import *
app = Flask(__name__)




#print(all)
#print(len(all))
#print(all[1][0])
stock=Stock('stock.xlsx')
all=stock.get_db()
#style="background-color:{%if cell[2]!='None'%}{{colors[int(cell[2])]}}{% endif %}"



@app.route('/',methods=['POST','GET'])
def main():
    print(stock.get_db())
    return render_template("index.html",all=all,print=print,colors=['white','#FFFFCC','#CC9966','#FF9966'],int=int)

@app.route('/swap',methods=['POST','GET'])
def swap():
    stock.movement()
    return redirect ('/')
@app.route('/add_quantity',methods=['POST','GET'])
def add_quantity():
    all=stock.get_db()
    for i in all:
        if i[1] == 0:
            stock.add(i[0], rand_quant(10, 50),rand_type())
    return redirect('/')

@app.route('/remove_quantity',methods=['POST','GET'])
def remove_quantity():
    n = 0
    while n < 30:
        while True:
            rand_cell = rand_id()
            rand_cell_quantity = stock.get_cell_quantity(rand_cell)
            if rand_cell_quantity > 0:
                rand_quantity = rand_quant(1, 10)
                stock.get(rand_cell, rand_quantity)
                break
        
        n += 1
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)