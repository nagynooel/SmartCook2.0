window.addEventListener("load", () => {
    let instruction_count = 0

    document.querySelectorAll("#instruction-container .instruction-input-group").forEach(item => {
        instruction_count++
        item.querySelector(".instruction-number").innerHTML = instruction_count + "."
    })

    const canvas = document.getElementById("macronutrients-chart");

    Chart.defaults.color = "#fff"

    // center text plugin
    const centerText = {
        id: "centerText",
        afterDatasetsDraw(chart, args, pluginOptions) {
            const { ctx, data } = chart
            
            const text = "240 kcal"

            const x = chart.getDatasetMeta(0).data[0].x
            const y = chart.getDatasetMeta(0).data[0].y

            ctx.save()
            ctx.textAlign = "center"
            ctx.textBaseline = "middle"
            ctx.font = "bold 60px roboto"
            ctx.fillText(text, x, y)
        }
    }

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: ["Protein", "Fat", "Carbs"],
            datasets: [{
                label: 'grams',
                data: [1,1,1],
                backgroundColor: [
                    'rgb(54, 162, 235)',
                    'rgb(255, 99, 132)',
                    'rgb(255, 205, 86)'
                ],
                cutout: "80%",
                borderWidth: 0,
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                }
            },
            events: [],
            animation: false
        },
        plugins: [centerText]
    });

})