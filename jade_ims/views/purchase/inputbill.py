from flask import Blueprint, render_template, request, redirect, url_for, flash
from jade_ims.models import db, InputBill, Supplier, Product
import datetime

inputbill = Blueprint('inputbill', __name__)


@inputbill.route('/purchase/input')
def list_input():
    data = []
    product_data = Product.query.all()
    inputbill_data = InputBill.query.all()
    for i in inputbill_data:
        data.append(
            {
                "ID": i.ID,
                "Name": Product.query.get(i.Product_ID).Name,
                "Supplier_Name": Supplier.query.get(
                    Product.query.get(i.Product_ID).Supplier_ID
                ).Name,
                "Quantity": i.Quantity,
                "Price": i.Price,
                "DateTime": i.DateTime,
                "Remark": i.Remark
            }
        )
    return render_template('purchase/inputbill.html',
                           product_data=product_data,
                           data=data
                           )


@inputbill.route('/purchase/input/add', methods=['POST'])
def add_input():
    form = request.form
    if request.method == 'POST':
        print(form)
        inputbill = InputBill(
            Product.query.filter_by(Name=form['product_name']).first().ID,
            int(form['quantity']),
            float(form['price']),
            datetime.datetime.strptime(form['datetime'], "%Y-%m-%d %H:%M"),
            form['product_remark']
        )
        try:
            db.session.add(inputbill)
            db.session.commit()
            flash('进货单添加成功!', 'success')
        except:
            db.session.rollback()
            flash('输入不合法, 请重新输入!', 'danger')
    return redirect(url_for('inputbill.list_input'))


@inputbill.route('/purchase/input/del', methods=['POST'])
def del_input():
    data = request.form.getlist('inputbill_check')
    if request.method == 'POST':
        for i in data:
            db.session.delete(InputBill.query.get(int(i)))
            db.session.commit()
        flash('进货单删除成功!', 'success')
    return redirect(url_for('inputbill.list_input'))
