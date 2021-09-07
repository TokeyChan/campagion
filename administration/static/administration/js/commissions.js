window.addEventListener('load', () => {
    const tds = document.getElementsByTagName("td");
    const month = new Date().getMonth() + 1;
    for (const td of tds) {
        if (td.dataset.month == month) {
            td.classList.add('present');
        } else if (td.dataset.month < month) {
            td.classList.add('past')
        } else {
            td.classList.add('future');
        }
        if (!td.dataset.commission_id) {
            td.classList.add('disabled');
        }
        td.addEventListener('click', () => {
            const id = td.dataset.commission_id;
            if (id) {
                send_request("/management/commissions/js/" + id, "GET", null, get_commission_data);
            }
        });
    }
});

function get_commission_data(raw_data) {
    var data = JSON.parse(raw_data);
    document.getElementById('insight_title').textContent = "Provision " + data['month'] + "/" + data['year'];

    const table = document.getElementById('insight_table');
    var rows = table.rows;

    for (let i = 1; i < rows.length; i++) {
        table.deleteRow(i);
    }

    for (const campaign of data['campaigns']) {
        const row = document.createElement('tr');
        var tds = [
            campaign['client'],
            campaign['name'],
            campaign['budget'],
            campaign['campagion_budget'],
            campaign['commission_amount']
        ];
        for (const td of tds) {
            let elem = document.createElement('td');
            elem.textContent = td;
            row.appendChild(elem);
        }
        table.appendChild(row);
    }
    table.style.display = "";
}