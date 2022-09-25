$(document).ready(
    function () {
        document.querySelector('#text').disabled = false
    }
)

function addTask() {
    let text = $("#text").val();
    let priority = $("#priority").val();
    let csrf = $('[name=csrfmiddlewaretoken]').val();
    if (text) {
        $.ajax({
            type: "POST",
            url: "/ajax/add-task/",
            data: {
                csrfmiddlewaretoken: csrf,
                text: text,
                priority: priority,
            },
            success: function (result) {
                $("#text").val('')
                $("#priority").val("Low")
                let priority_class = 'bg-info'
                if (priority === 'Low') {
                    priority_class = 'bg-success'
                } else if (priority === 'Middle') {
                    priority_class = 'bg-warning'
                } else if (priority === 'High') {
                    priority_class = 'bg-danger'
                }

                let tr = $('<tr> </tr>')
                let checkbox = $(`<td><div class="animated-checkbox"> <label><input type="checkbox" value="${result['task_id']}" class="task-done"><span class="label-text"></span> </label> </div>  </td>`)
                let taskText = $(`<td class=" text-left" id="task-text-${result['task_id']}">${text}</td>`)
                let priority_tag = $(`<td class=" text-left" ><span class="badge text-light p-2 ${priority_class}"> ${priority} priority </span></td>`)
                let date = $(`<td> ${result['task_date']} ${result['task_time']} </td>`)
                let actions = $(`<td> <div class="d-flex justify-content-center align-items-center">  <a href="#" class="action"><i class="fa-solid fa-pen text-info mr-3"></i></a> <a href="#" class="action"><i class="fa-solid fa-trash-can text-danger "></i></a> </div> </td>`)

                tr.append(checkbox)
                tr.append(taskText)
                tr.append(priority_tag)
                tr.append(date)
                tr.append(actions)
                $('#task-list').append(tr)

                let checkButton = document.querySelector(`[value="${result['task_id']}"]`)
                checkButton.addEventListener('click', checkTask)

                $.notify({
                    title: "Message : ",
                    message: result['message'],
                    icon: "fa-solid fa-check mr-2"
                }, {
                    type: "success"
                });
            },
            error: function (xhr, status, error) {
                $.notify({
                    title: "Error : ",
                    message: xhr.responseJSON.error,
                    icon: "fa-solid fa-xmark mr-2"
                }, {
                    type: "danger"
                });
            }
        })
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Alert...',
            text: 'Text must be filled out',
        })
    }
}

// $("#add-tasks").submit(addTask)
$('#add-task').click(addTask)

$("#text").keyup(function (event) {
    if (event.keyCode === 13) {
        addTask()
    }
});

function checkTask() {
    let csrf = $('[name=csrfmiddlewaretoken]').val();
    let status = this.checked
    let task_id = this.value
    $.ajax({
        type: "POST",
        url: "/ajax/check-task/",
        data: {
            csrfmiddlewaretoken: csrf,
            status: status,
            task_id: task_id,
        },
        success: function (result) {
            if (status) {
                $(`#task-text-${task_id}`).addClass('line-trough')
            } else {
                $(`#task-text-${task_id}`).removeClass('line-trough')
            }
            $.notify({
                    title: "Message : ",
                    message: result['message'],
                    icon: "fa-solid fa-check mr-2"
                }, {
                    type: "success"
                }
            );
        }, error: function (xhr, status, error) {
            $.notify({
                title: "Error : ",
                message: xhr.responseJSON.error,
                icon: "fa-solid fa-xmark mr-2"
            }, {
                type: "danger"
            });
        }
    })
}


let checkboxes = document.querySelectorAll('.task-done')

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', checkTask)
})