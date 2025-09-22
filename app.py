from flask import Flask, jsonify, request # pyright: ignore[reportMissingImports]

app = Flask(__name__)

# Banco de dados em memória (simples, só para exemplo)
users = {"admin": "123"}  # usuário fixo
tasks = []  # lista de tarefas


# ----------------- Rotas de Login -----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        return jsonify({"message": "Login realizado com sucesso!"})
    return jsonify({"error": "Credenciais inválidas"}), 401


# ----------------- Rotas de Tarefas (API REST) -----------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    task = {"id": len(tasks) + 1, "title": data["title"], "done": False, "priority": data.get("priority", "normal")}
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["status"] = data.get("status", task["status"])
            return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Tarefa removida com sucesso!"})
    return jsonify({"error": "Tarefa não encontrada"}), 404


# ----------------- Rotas extras para teste no navegador -----------------
@app.route("/")
def home():
    return jsonify({"message": "API do TechFlow Task Manager está rodando!"})


# Criar tarefa via navegador (exemplo: /add_task?title=Estudar)
@app.route("/add_task")
def add_task():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Informe o parâmetro ?title=... na URL"}), 400
    
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": "A Fazer"
    }
    tasks.append(task)
    return jsonify(task)


# Atualizar status via navegador (exemplo: /update_task?id=1&status=Concluido)
@app.route("/update_task")
def update_task_query():
    task_id = request.args.get("id", type=int)
    status = request.args.get("status")

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404


# Remover tarefa via navegador (exemplo: /delete_task?id=1)
@app.route("/delete_task")
def delete_task_query():
    task_id = request.args.get("id", type=int)

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Tarefa removida com sucesso!"})
    return jsonify({"error": "Tarefa não encontrada"}), 404


# ----------------- Executar aplicação -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
