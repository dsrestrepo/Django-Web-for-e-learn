document.addEventListener('DOMContentLoaded', function() {
    const trainX = [
        3.3,
        4.4,
        5.5,
        6.71,
        6.93,
        4.168,
        9.779,
        6.182,
        7.59,
        2.167,
        7.042,
        10.791,
        5.313,
        7.997,
        5.654,
        9.27,
        3.1
      ];
    const trainY = [
        1.7,
        2.76,
        2.09,
        3.19,
        1.694,
        1.573,
        3.366,
        2.596,
        2.53,
        1.221,
        2.827,
        3.465,
        1.65,
        2.904,
        2.42,
        2.94,
        1.3
    ];
    let table_content = ""
    for (i=0; i<17; i++){
    table_content =  `${table_content} <tr><td>${trainX[i]}</td><td id="x-${i}" >${trainY[i]}</td></tr>`;
    }
    document.querySelector('#data-table').innerHTML = table_content
    
    initial_table(trainX,trainY);

});

//function initial
function initial_table(trainX,trainY){
    const model = tf.sequential();
    model.add(tf.layers.dense({units: 1, inputShape: [1]}));

    // Prepare the model for training: Specify the loss and the optimizer.
    model.compile({loss: 'meanSquaredError', optimizer: 'sgd'});

    // Generate some synthetic data for training.
    const xs = tf.tensor2d(trainX, [17, 1]);
    const ys = tf.tensor2d(trainY, [17, 1]);

    // Train the model using the data.
    model.fit(xs, ys,{
        epochs: 32,
        batchSize: 2        
      }).then(() => {
        // Use the model to do inference on a data point the model hasn't seen before:
        // Open the browser devtools to see the output
        model.predict(tf.tensor2d([16], [1, 1])).print();
        print_regression(trainX,trainY,model)
    });

}

//funtion print
function print_regression(trainX,trainY,model){
    async function plot() {
        let plotData = [];
    
        for (let i = 0; i < trainY.length; i++) {
            plotData.push({ x: trainX[i], y: trainY[i] });
    }
    
    var ctx = document.getElementById("myChart").getContext("2d");
    
    var scatterChart = new Chart(ctx, {
        type: "line",
        data: {
        datasets: [
            {
            label: "Training Data",
            showLine: false,
            data: plotData,
            fill: false,
            backgroundColor:'black'
            },
            {
            label: "regression",
            data: [
                {
                x: 0,
                y: model.predict(tf.tensor2d([0], [1, 1])).dataSync()[0]
                },
                {
                x: 11,
                y: model.predict(tf.tensor2d([9], [1, 1])).dataSync()[0]
                }
            ],
    
            type: "line",
            borderColor: "red",
            fill: false
            }
        ]
        },
        options: {
        animation: false,
        scales: {
            yAxes: [
                {
                ticks: {
                    max: 5
                }
                }
            ],
            xAxes: [
            {
                type: "linear",
                position: "bottom"
            }
            ]
        }
        }
    });
    }
    plot();
}