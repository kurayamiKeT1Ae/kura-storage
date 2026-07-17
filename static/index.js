
const files_div = document.getElementById('files');

const upload_form = document.getElementById('upload-form');
const upload_input = document.getElementById('upload-input');
const upload_button = document.getElementById('upload-button');
const upload_message = document.getElementById('upload-message');

function show_message(message, type){
    upload_message.innerHTML = `
    ${message}
    <span id="message-close">&times;</span>
    `;
    upload_message.className = `show ${type}`;

    document.getElementById("message-close").addEventListener('click', () => {
        upload_message.className = "";
        upload_message.innerHTML = "";
    });
}



async function post(url, body, form=false){
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json"
        }
    });

    return {
        ok: response.ok,
        data: await response.json()
    };
}

async function load_data(){
    const response = await fetch('/data');
    const data = await response.json();

    for (const file of data['files']){
        const file_div = document.createElement("div");
        file_div.className = "file";

        const file_span = document.createElement('span');
        file_span.textContent = file;
        file_span.className = "file-name";

        const download_button = document.createElement('button');
        download_button.textContent = "Download";
        download_button.className = "download-button";

        download_button.addEventListener("click", () => {
            window.location.href = `/download/${encodeURIComponent(file)}`;
        });

        const delete_button = document.createElement('button');
        delete_button.textContent = "Delete";
        delete_button.className = "delete-button";

        file_div.appendChild(file_span);
        file_div.appendChild(download_button);
        file_div.appendChild(delete_button);

        files_div.appendChild(file_div);

        delete_button.addEventListener("click", async (event) => {
            event.preventDefault();

            const response = await post('/delete', {file: file});

            if (response.ok){
                file_div.classList.add("removing");
                setTimeout(() => {
                    file_div.remove();
                }, 500);
            }
        })
    }
}


upload_button.addEventListener("click", async () => {
    event.preventDefault();

    const form_data = new FormData(upload_form);
    
    const response = await fetch("/upload", {
        method: "POST",
        body: form_data
    });
    const data = await response.json();

    if (response.ok){
        const file_div = document.createElement("div");
        file_div.className = "file";

        const file_span = document.createElement('span');
        const file_name = upload_input.files[0].name;
        file_span.textContent = file_name;
        file_span.className = "file-name";

        const download_button = document.createElement('button');
        download_button.textContent = "Download";
        download_button.className = "download-button";

        download_button.addEventListener("click", () => {
            window.location.href = `/download${encodeURIComponent(file)}`;
        });


        const delete_button = document.createElement('button');
        delete_button.textContent = "Delete";
        delete_button.className = "delete-button";


        file_div.appendChild(file_span);
        file_div.appendChild(download_button);
        file_div.appendChild(delete_button);

        files_div.appendChild(file_div);


        // message
        show_message(data.message, "success");

        delete_button.addEventListener("click", async (event) => {
            event.preventDefault();

            const response = await post('/delete', {file: file_name});

            if (response.ok){
                file_div.classList.add("removing");
                setTimeout(() => {
                    file_div.remove();
                }, 700);
            } 
        })
    } else if (400 < response.status < 500){
        show_message(data.message, "error");
    }

});

load_data();