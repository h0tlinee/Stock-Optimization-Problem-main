from Cell import *
from Optimizator import *
from Queue import *
from Stock import *
from flask import Flask, render_template, request, flash, redirect, url_for,json,jsonify
from input_handler import *







app = Flask(__name__)
app.config['SECRET_KEY'] = 'gfdgfdkgfdjfgd7fddjfd'




#print(all)
#print(len(all))
#print(all[1][0])

#style="background-color:{%if cell[2]!='None'%}{{colors[int(cell[2])]}}{% endif %}"

#todo:нарисовать большие ячейки(ряды,полки,маленькие ячейки),выбор файла перед отрисовкой всей хуйни, остальные кнопки при этом залочены(флаг)


stock=None
flag_loaded=False
flag_file=None
all=None
path=None

@app.route('/',methods=['POST','GET'])
def main():
    params=None
    if(stock!=None):
        print(stock.get_stock_params())
        params=stock.get_stock_params()
    
    #global flag_loaded
    if(flag_loaded):
        
        return render_template("index.html",all=all,print=print,colors=['white','#FFFFCC','#CC9966','#FF9966'],int=int,flag_loaded=flag_loaded,path=path,params=params)
    else:
        return render_template("index.html",print=print,colors=['white','#FFFFCC','#CC9966','#FF9966'],int=int,flag_loaded=flag_loaded,path=path,params=params)
    
@app.route('/db_load',methods=['POST','GET'])
def load_db():
    global flag_loaded,flag_file,stock,all,path
    if(path==None):
        flash('Ошибка! Сначала выберите файл')
        return redirect(url_for('main',stock=stock,all=all,flag_loaded=flag_loaded))
    else:
        stock=Stock(path)
        all=stock.get_db()
        print(request.input_stream)
        flag_loaded=True
        return redirect(url_for('main',stock=stock,all=all,flag_loaded=flag_loaded))

@app.route('/test', methods=['POST','GET'])
def test():
    global path
    output = request.get_json()
    print("Chosen file:")
    #print(output)
    path=output[12:]
    print(path)
    #print(type(output))
    #result = json.loads(output) 
    #print(result) 
    #print(type(result))
    return path

@app.route('/config_edit',methods=['POST','GET'])
def conf():
    global flag_loaded,flag_file,stock,all,path
    rows=(request.form['rows'])
    height=(request.form['height'])
    length=(request.form['length'])
    #flash(rows)
    #flash(height)
    #flash(length)
    #flash(path)
    if(rows=='' or height=='' or length==''):
        flash('Вы ввели конфигурацию не полностью! Повторите попытку')
        return redirect (url_for('main',all=all,stock=stock,flag_loaded=flag_loaded))
    rows_=int(rows)
    height_=int(height)
    length_=int(length)
    if(rows_<=0 or height_<=0 or length_<=0):
        flash('Вы ввели в конфигурации отрицательное число или ноль! Повторите попытку')
        return redirect (url_for('main',all=all,stock=stock,flag_loaded=flag_loaded))
    stock.set_stock_params(rows_,height_,length_,50)
    return redirect (url_for('load_db',all=all,stock=stock,flag_loaded=flag_loaded))
@app.route('/swap',methods=['POST','GET'])
def swap():
    global stock,all
    stock.movement()
    all=stock.get_db()
    #print(all)
    return redirect (url_for('main',all=all,stock=stock,flag_loaded=flag_loaded))
@app.route('/add_quantity',methods=['POST','GET'])
def add_quantity():
    global all,stock
    #all=stock.get_db()
    for i in all:
        if i[1] == 0:
            stock.add(i[0], rand_quant(10, 50),rand_type())
    #print(all)
    all=stock.get_db()
    return redirect(url_for('main',all=all,stock=stock,flag_loaded=flag_loaded))

@app.route('/remove_quantity',methods=['POST','GET'])
def remove_quantity():
    global stock,all
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
    all=stock.get_db()
    return redirect(url_for('main',all=all,stock=stock,flag_loaded=flag_loaded))

if __name__ == "__main__":
    app.run(debug=True)