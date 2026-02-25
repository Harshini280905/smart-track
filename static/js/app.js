document.addEventListener("DOMContentLoaded", function () {

    if (document.getElementById("task-list")) {
        fetch("/api/tasks")
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById("task-list");
                data.forEach(task => {
                    const li = document.createElement("li");
                    li.innerText = `${task.title} - ${task.status}`;
                    list.appendChild(li);
                });
            });
    }

    if (document.getElementById("project-list")) {
        fetch("/api/projects")
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById("project-list");
                data.forEach(project => {
                    const li = document.createElement("li");
                    li.innerText = `${project.name} (Owner: ${project.owner})`;
                    list.appendChild(li);
                });
            });
    }

});