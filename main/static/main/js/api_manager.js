const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
  };
const CHART_COLOR_NAMES = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey'];

class ApiManager {
    constructor(campaign_id) {
        this.graph = null;
        this.current_mc_index = -1; //-1 == Gesamt, alles andere ist dann der Index auf dem Minicampaign Array
        this.minicampaigns = [];
        this.campaign_id = campaign_id;
        this.setup();
    }
    setup() {
        this.ctx = document.getElementById('api_graph').getContext('2d');
        this.table = document.getElementById('api_table');
        this.table_manager = new TableManager(this.table);

        this.get_minicampaigns().then((result) => {
            this.minicampaigns = result;
            this.switch_view();
        });

        this.startdate_picker = document.getElementById('startdate_picker');
        this.enddate_picker = document.getElementById('enddate_picker');
        this.left_arrow = document.getElementById('left_arrow');
        this.left_arrow_div = document.getElementById('minicampaign_left_name')
        this.title = document.getElementById('minicampaign_title');
        this.right_arrow = document.getElementById('right_arrow');
        this.right_arrow_div = document.getElementById('minicampaign_right_name');

        this.create_graph(this.startdate_picker.value, this.enddate_picker.value);
        this.startdate_picker.addEventListener('change', () => {
            this.update_graph(this.startdate_picker.value, this.enddate_picker.value);
        });
        this.enddate_picker.addEventListener('change', () => {
            this.update_graph(this.startdate_picker.value, this.enddate_picker.value);
        });
        this.update_graph(this.startdate_picker.value, this.enddate_picker.value);
        this.left_arrow.addEventListener('click', () => { this.switch_left() });
        this.left_arrow_div.addEventListener('click', () => { this.switch_left() });
        this.right_arrow.addEventListener('click', () => { this.switch_right() });
        this.right_arrow_div.addEventListener('click', () => { this.switch_right() });
    }
    switch_view() {
        this._name_logic();
        this.get_sum(this.current_mc_index == -1 ? -1 : this.minicampaigns[this.current_mc_index]['id']).then((result) => {
            this.table_manager.render(result);
        });
        this.update_graph(this.startdate_picker.value, this.enddate_picker.value);
    }
    _name_logic() {
        var title;
        try {
            title = this.minicampaigns[this.current_mc_index]['name'];
        } catch { title = "Gesamt";}
        this.title.textContent = title;
        const left_index = this.current_mc_index - 1;
        const right_index = this.current_mc_index + 1;
        var left_name = "";
        var right_name = "";

        if (left_index == -1) {
            left_name = "Gesamt";
        } else if (left_index >= 0 && left_index < this.minicampaigns.length) {
            left_name = this.minicampaigns[left_index]['name'];
        }
        if (right_index < this.minicampaigns.length) {
            right_name = this.minicampaigns[right_index]['name'];
        }
        if (left_name) {
            this.left_arrow_div.textContent = left_name;
            this.left_arrow_div.style.display = "";
            this.left_arrow.style.display = "";
        } else {
            this.left_arrow_div.style.display = "none";
            this.left_arrow.style.display = "none";
        }
        if (right_name) {
            this.right_arrow_div.textContent = right_name;
            this.right_arrow_div.style.display = "";
            this.right_arrow.style.display = "";
        } else {
            this.right_arrow_div.style.display = "none";
            this.right_arrow.style.display = "none";
        }
    }
    switch_left() {
        this.current_mc_index--;
        this.switch_view();
    }
    switch_right() {
        this.current_mc_index++;
        this.switch_view();
    }
    create_graph() {
        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                lables: ['1', '2', '3', '4', '5'],
                datasets: []
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'API-DATEN'
                    }
                },
                scales: {
                    big: {
                        type: 'linear',
                        display: true,
                        position: 'left'
                    },
                    /*
                    small: {
                        type: 'logarithmic',
                        display: true,
                        'position': 'right'
                    }
                    */
                }
            }
        });
    }
    async update_graph(start_date, end_date) {
        var datasets_hidden = [];
        for (let i = 0; i < this.chart.data.datasets.length; i++) {
            datasets_hidden[i] = this.chart.getDatasetMeta(i).hidden == true;
        }
        const minicampaign_id = this.current_mc_index == -1 ? -1 : this.minicampaigns[this.current_mc_index]['id'];
        const datasets = await this.get_dataset(start_date, end_date, minicampaign_id);
        this.chart.data.labels = datasets[0]['data'].map(t => t['x']);
        this.chart.data.datasets = datasets;

        for (let i = 0; i < datasets_hidden.length; i++) {
            this.chart.getDatasetMeta(i).hidden = datasets_hidden[i];
        }
        if (datasets_hidden.length == 0) //beim ersten Durchlauf
            this.chart.update();
        else
            this.chart.update('none');
    }
    async get_dataset(start_date, end_date, minicampaign_id) {
        const data = await this.get_api_stats(start_date, end_date, minicampaign_id);
        var datasets = [];

        for (let i = 0; i < data['datasets'].length; i++) {
            const set = data['datasets'][i];
            const color = CHART_COLORS[CHART_COLOR_NAMES[i]];
            var obj = {
                'label': set['label'],
                'data': set['data'],
                'borderColor': color,
                'backgroundColor': color,
            }
            datasets.push(obj);
        }
        return datasets;
    }
    get_minicampaigns() {
        const request = new HttpRequest();
        request.open('GET', API_URLS['minicampaigns'] + "?campaign_id=" + CAMPAIGN_ID);
        return request.send();
    }
    get_sum(minicampaign_id) {
        const request = new HttpRequest();
        if (minicampaign_id == -1) { //GESAMT
            request.open('GET', API_URLS['sum'] + "?campaign_id=" + this.campaign_id);
        } else {
            request.open('GET', API_URLS['sum_minicampaign'] + "?minicampaign_id=" + minicampaign_id);
        }
        return request.send()
    }
    get_api_stats(start_date, end_date, minicampaign_id) {
        const request = new HttpRequest();
        if (minicampaign_id == -1) {
            request.open('GET', API_URLS['stats'] + "?start_date=" + start_date.toString() + "&end_date=" + end_date.toString() + "&campaign_id=" + this.campaign_id);
        } else {
            request.open('GET', API_URLS['stats_minicampaign'] + "?start_date=" + start_date.toString() + "&end_date=" + end_date.toString() + "&minicampaign_id=" + minicampaign_id);
        }
        return request.send();
    }
}


class TableManager {
    static TABLE_ROWS = [
        [ 'impressions', 'Impressions'],
        [ 'revenue', 'Kosten (in €)'],
        [ 'clicks', 'Clicks'],
        [ 'conversions', 'Conversions'],
        [ 'ctr', 'CTR'],
        [ 'ecpm', 'eCPM'],
        [ 'ecpc', 'eCPC']
    ]
    constructor(table) {
        this.table = table;

    }
    render(data) {
        while (this.table.firstChild) {
            this.table.removeChild(this.table.firstChild);
        }
        for (const row of TableManager.TABLE_ROWS) {
            var tr = document.createElement('tr');
            var th = document.createElement('th');
            var td = document.createElement('td');
            var input = document.createElement('input');
            input.type = 'text';
            input.readOnly = true;
            input.value = data[row[0]];
            td.appendChild(input);

            th.textContent = row[1];

            tr.appendChild(th);
            tr.appendChild(td);
            this.table.appendChild(tr);
        }
    }
}

class HttpRequest extends XMLHttpRequest {
    constructor() {
        super();
    }
    send() {
        return new Promise((resolve, reject) => {
            this.addEventListener('load', () => {
                if (this.status >= 200 && this.status < 300) {
                    const json = JSON.parse(this.responseText);
                resolve(json);
                } else {
                    console.warn(this.responseText);
                    reject();
                }
            });
            XMLHttpRequest.prototype.send.call(this);
        });
    }
}