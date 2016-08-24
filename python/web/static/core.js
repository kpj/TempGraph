class Plot {
  constructor(data) {
    let ctx = document.getElementById('chart');
    this.obj = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.x,
        datasets: data.sets
      }
    });
  }

  update(data) {
    let new_data = this.compute_new_data(data);

    for(let ele of new_data) {
      this.obj.data.labels.push(ele.x);
      this.obj.data.datasets[0].data.push(ele.y);
    }

    var max_data_points = 60;
    var nr_to_splice = this.obj.data.datasets[0].data.length - max_data_points;

    if(nr_to_splice > 0) {
      this.obj.data.labels.splice(0, nr_to_splice);
      this.obj.data.datasets[0].data.splice(0, nr_to_splice);
    }
    this.obj.update();
  }

  compute_new_data(data) {
    let obj_last_ts = this.obj.data.labels[this.obj.data.labels.length-1];
    let idx = data.x.indexOf(obj_last_ts);

    let new_data = [];
    for(let i = idx; i < data.x.length; i++) {
      new_data.push({
        x: data.x[i],
        y: data.sets[0].data[i]
      });
    }

    return new_data;
  }
}

let plot = undefined;
const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('update', function(data) {
  plot.update(JSON.parse(data));
});

const callback = function(data) {
  plot = new Plot(data);
}

d3.json('/data', callback);
