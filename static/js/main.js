window.onload = function(){
    const div_comp = document.querySelector(`#comp-dataset`);
    div_comp.classList.remove('d-none');
}

function checkManualInput(event){
//    console.log(event.target.parentNode);
    if (event.target.value == 'user-entry'){
        event.target.parentNode.parentNode.querySelector('.manual-input').disabled = false;
    }
}

function checkScatter(){
    const chart_type = document.querySelector('#chart-type');
    const reg_sw = document.querySelector('#addRegression');
    const y_val = document.querySelector('#y-col');
    if (chart_type.value == "2"){
        reg_sw.parentNode.classList.remove('d-none');
        y_val.classList.remove('d-none');
    }
    else if (chart_type.value == "4"){
        y_val.classList.add('d-none');
        reg_sw.parentNode.classList.add('d-none');
    }
    else{
        reg_sw.parentNode.classList.add('d-none');
        y_val.classList.remove('d-none');
    }
}

function submitForm(){
    const cols = document.querySelectorAll('.column-fill');
    const dashboard_name = document.querySelector('#dashboard-name').value;
    const data = [];
    for (let i=0; i<cols.length; i++){
        const col_data = {};
        col_data.column_name = cols[i].querySelector('.column-name').value;
        col_data.selection = cols[i].querySelector('.fill-select').value;
        col_data.manual_input = cols[i].querySelector('.manual-input').value;
        data.push(col_data);
    }
    fetch('/process-value', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'data': data, 'dashboard_name': dashboard_name,
        'scale': document.querySelector('#addScaling').checked, 'scale-type': document.querySelector('#scale-select').value})
    }).then(response => response).then(resp_data => {
        if (resp_data.status == 200){
            window.location = `/dashboard/${dashboard_name}`;
        }
    })
}

function toggleScaling(){
    document.querySelector('#scale-select').classList.toggle('d-none');
}

function changeTab(event){
    const btn = event.target;
    const curr_div = document.querySelector('.show.active');
    const curr_btn = document.querySelector('.nav-link.active');
    const btn_div = document.querySelector(`#${btn.dataset.tab_id}`);
    curr_div.classList.remove('show', 'active');
    curr_btn.classList.remove('active');
    btn_div.classList.add('show', 'active');
    btn.classList.add('active');
}
const file_inp = document.querySelector('#data-input');
//file_inp.onchange = function(){
//    const formData = new FormData();
//    const spinner = document.querySelector('.spinner-grow');
//    spinner.style.display = 'flex';
//    formData.append('data-inp', file_inp.files[0]);
//     fetch('/', {
//        method: 'POST',
//        body: formData,
//    }).then(response => response.json())
//          .then(raw_data => {
//                const data = JSON.parse(raw_data.df);
//                const datadiv = document.querySelector('#data-div');
//                const cols = Object.keys(data);
//                const rows = Object.keys(data[cols[0]]);
//
//                const table = document.createElement('table');
//                table.classList.add('table', 'table-dark', 'table-hover');
//                const thead = document.createElement('thead');
//                thead.classList.add('table-light', 'table-cols');
//                const tr = document.createElement('tr');
//                const th = document.createElement('th');
//                th.innerText = '#';
//                tr.appendChild(th);
//
//                for (let j=0; j<cols.length; j++){
//                    const th = document.createElement('th');
//                    th.innerText = cols[j];
//                    tr.appendChild(th);
//                }
//                thead.appendChild(tr);
//                table.appendChild(thead);
//
//                const tbody = document.createElement('tbody');
//
//                for(let i=0; i<rows.length; i++){
//                    const tr = document.createElement('tr');
//                    const td = document.createElement('td');
//                    td.innerText = i;
//                    tr.appendChild(td);
//
//                    for (let j=0; j<cols.length; j++){
//                        const td = document.createElement('td');
//                        td.innerText = data[cols[j]][rows[i]];
//                        tr.appendChild(td);
//                    }
//                    tbody.appendChild(tr);
//                }
//                table.appendChild(tbody);
//                datadiv.appendChild(table);
//                const heatmap = JSON.parse(raw_data.heatmap);
//                Plotly.plot('heatmap-div', heatmap, {});
//                spinner.style.display = 'none';
//          })
//}

function showComponent(event){
    const btn = event.target;
//    console.log(btn);
    const id = btn.dataset.div_id;
    const components = document.querySelectorAll('.component');
    console.log(components);
    const div_comp = document.querySelector(`#comp-${id}`);
    for (let i=0; i<components.length; i++){
        const comp_id = `#comp-${components[i].dataset.div_id}`;
        console.log(comp_id);
        const div_comp_ind = document.querySelector(comp_id);
        console.log(div_comp_ind);
        div_comp_ind.classList.add('d-none');
    }
    console.log(div_comp);
    div_comp.classList.remove('d-none');
}