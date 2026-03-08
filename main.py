from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():

  try:
      con = sqlite3.connect("ecom.db")
      con.row_factory = sqlite3.Row
      cur = con.cursor()

      cur.execute("""select * from product""")
      rows = cur.fetchall()
      print(rows)

      con.commit()

  except Exception as e:
     print(e)

  finally:
     con.close()

  return render_template("index.html", rows = rows)

@app.route("/create", methods = ["POST","GET"])
def create():
  
  if request.method == "POST":
      try:
        con = sqlite3.connect("ecom.db")
        cur = con.cursor()

        cur.execute("""create table if not exists product(
                    title varchar(100),
                    content varchar(450),
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT
        );""")

        title = request.form.get("Title")
        content = request.form.get("Content")

        cur.execute("""
                    INSERT INTO product (title, content) 
                    VALUES (?, ?);
                """, (title, content))
        
        cur.execute("""select * from product""")

        result = cur.fetchall()
        print(result)

        con.commit()
      except Exception as e:
        print(f"DataBase Error, {e}")
        con.rollback()
      finally:
        con.close()

  return render_template("create.html")

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete(product_id):
    try:
        con = sqlite3.connect("ecom.db")
        cur = con.cursor()

        # Delete the specific product using its ID
        # The comma in (product_id,) is required to make it a valid Python tuple!
        cur.execute("DELETE FROM product WHERE product_id = ?", (product_id,))
        
        # Save the changes
        con.commit()
        print(f"Successfully deleted product ID: {product_id}")

    except Exception as e:
        print(f"Database Error: {e}")
        con.rollback()
        
    finally:
        con.close()

    # Redirect the user back to the home page route to see the updated list
    return redirect(url_for('home'))

@app.route("/update/<int:product_id>", methods=["GET", "POST"])
def update(product_id):
    con = sqlite3.connect("ecom.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == "POST":
        try:
            new_title = request.form.get("Title")
            new_content = request.form.get("Content")

            cur.execute("""
                UPDATE product 
                SET title = ?, content = ? 
                WHERE product_id = ?
            """, (new_title, new_content, product_id))
            
            con.commit()
            print("Product updated successfully!")
            
        except Exception as e:
            print(f"Database Error: {e}")
            con.rollback()
        finally:
            con.close()
            
        return redirect(url_for('home'))

    else:
        cur.execute("SELECT * FROM product WHERE product_id = ?", (product_id,))
        product_to_edit = cur.fetchone() 
        con.close()

        return render_template("update.html", product=product_to_edit)

@app.route("/cart/<int:product_id>", methods = ["POST", "GET"])
def cart(product_id):
    try:
        con = sqlite3.connect("ecom.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""select * from product where product_id = ?""",(product_id,))
        show = cur.fetchone()

        if show:
    

            cur.execute("""create table if not exists cart(
                        title varchar(100),
                        content varchar(450),
                        product_id int
            );""")

            cur.execute("""insert into cart(title, content, product_id) values(?,?,?)""", (show['title'], show['content'], show['product_id']))

            con.commit()  
            print(f"Successfully added {show['title']} in my cart")

        else:
            print("Error: Product Not Found")

    except Exception as e:
        print(e)
        con.rollback()

    finally:
        con.close()  
    
    return redirect(url_for('home'))

@app.route("/cart")
def cart_page():
    try:
        con = sqlite3.connect("ecom.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("""select * from cart""")
        rows = cur.fetchall()

        con.commit()

    except Exception as e:
        print(e)
        con.rollback()
    
    finally:
        con.close()
    
    return render_template("cart.html", rows = rows)

@app.route("/remove/<int:product_id>", methods = ["POST", "GET"])
def remove(product_id):
    try:
        con = sqlite3.connect("ecom.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("delete from cart where product_id = ?", (product_id,))

        con.commit()

    except Exception as e:
        print(e)
        con.rollback()
        
    finally:
        con.close()

    return redirect(url_for('cart_page'))

app.run(debug=True)

