from flask import Flask, render_template, url_for, request, redirect
from model import Todo, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        db.add(new_task)
        db.commit()

        return redirect("/")
    else:
        tasks = db.query(Todo).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = db.query(Todo).get(id)

    db.delete(task_to_delete)
    db.commit()

    return redirect("/")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = db.query(Todo).get(id)

    if request.method == "POST":
        task.content = request.form["content"]
        db.commit()
        return redirect("/")
    else:
        return render_template("/update.html", task=task)


if __name__ == '__main__':
    app.run()