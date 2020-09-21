//define margin
let margin = {
    top: 50,
    right: 50,
    bottom: 30,
    left: 50
};

//Set graph size
let svgWidth = 800;
let svgHeight = 450;
let graphWidth = svgWidth - margin.left - margin.right;
let graphHeight = svgHeight - margin.bottom - margin.top;

//Create a date parser for our data (parse time into formatted strings)
let dateParse = d3.timeParse("%d-%m-%Y");
let monthParse = d3.timeParse("%m-%Y");

//Create scale for our axes
let x = d3.scaleTime().range([0, graphWidth]);
let y = d3.scaleLinear().range([graphHeight, 0]);

//Create axes
let xAxis = d3.axisBottom().scale(x);
let yAxis = d3.axisLeft().scale(y);

//Functions to draw line based on data (d) received
let borrowLine = d3.line().x(function(d) { return x(d.date) }).y(function(d) { return y(d.borrow_count) });
let returnLine = d3.line().x(function(d) { return x(d.date) }).y(function(d) { return y(d.return_count) });

//Create svgs (this is where we'll draw our graphs)
let svg = d3.select("#graphDailyDiv")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

let monthSvg = d3.select("#graphMonthlyDiv")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//Draw daily graph
function drawDailyGraph(data) {
    // For each row in the data, parse the date
    // and use + to make sure data is numerical
    data.forEach(function(d) {
        d.date = dateParse(d.date);
        d.borrow_count = +d.borrow_count;
        d.return_count = +d.return_count;
    });

    //Set our scale to match the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([d3.min(data, function(d) {
        return Math.min(d.borrow_count, d.return_count) }),
        d3.max(data, function(d) {
            return Math.max(d.borrow_count, d.return_count) })]);

    // Add the highLine as a green line
    svg.append("path")
        .style("stroke", "green")
        .style("fill", "none")
        .attr("class", "line")
        .attr("d", borrowLine(data));

    // Add the closeLine as a blue dashed line
    svg.append("path")
        .style("stroke", "blue")
        .style("fill", "none")
        .style("stroke-dasharray", ("3, 3"))
        .attr("d", returnLine(data));

    //Draw dots and add event listenner to be more interactive
    svg.selectAll('circle.borrow')
        .data(data)
        .enter()
        .append('circle')
        .attr("class", "borrow")
        .attr("cx", function(d) { console.log(x(d.date));return x(d.date) })
        .attr("r", 5)
        .attr("cy", function(d) { return y(d.borrow_count) })
        .style("fill", function() { return 'green' })
        .on('mouseover', handleBorrowLineHover)
        .on('mouseout', handleBorrowLineOut)
        .exit();

    //Same as above
    svg.selectAll('circle.return')
        .data(data)
        .enter()
        .append('circle')
        .attr("class", "return")
        .attr("cx", function(d) { return x(d.date) })
        .attr("r", 5)
        .attr("cy", function(d) { return y(d.return_count) })
        .style("fill", function() { return 'blue' })
        .on('mouseover', handleReturnLineHover)
        .on('mouseout', handleReturnLineOut)
        .exit();

    //Draw the x axis we have created above
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + graphHeight + ")")
        .call(xAxis);

    //Add a label for our axis
    svg.append("text")
        .attr("transform", "translate(" + (graphWidth/2) + ", " + (graphHeight + margin.top - 20) + ")")
        .style("text-anchor", "middle")
        .attr("font", "18px arial")
        .text("Date");

    //Draw the y axis we have created above
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    //Add a label for our axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (graphHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .attr("font", "18px arial")
        .text("Number of cars");

    //Add a text element to annotate our borrowed cars line
    svg.append("text")
        .attr("transform", "translate("+(graphWidth - 10)+","+ (y(data[data.length-1].borrow_count) - 15)+")")
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .style("fill", "green")
        .text("Borrow");

    //Add a text element to annotate out returned cars line
    svg.append("text")
        .attr("transform", "translate("+(graphWidth - 10)+","+(y(data[data.length-1].return_count) - 15)+")")
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .style("fill", "red")
        .text("Return");
}


//Draw monthly analytics from graph
function drawMonthlyGraph(data) {
    data.forEach(function(d) {
        d.month = monthParse(d.month);
        d.borrow_count = +d.borrow_count;
        d.return_count = +d.return_count;
    });

    x.domain(d3.extent(data, function(d) { return d.month; }));
    y.domain([0, d3.max(data, function(d) { return Math.max(d.borrow_count, d.return_count) })]);


    monthSvg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + graphHeight + ")")
        .call(xAxis);

    monthSvg.append("text")
        .attr("transform", "translate(" + (graphWidth/2) + ", " + (graphHeight + margin.top - 20) + ")")
        .style("text-anchor", "middle")
        .attr("font", "18px arial")
        .text("Month");

    monthSvg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    monthSvg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (graphHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .attr("font", "18px arial")
        .text("Number of cars");

    //Draw bar chart and add event listener
    monthSvg.selectAll('bar.borrow')
        .data(data)
        .enter()
        .append('rect')
        .attr("x", function(data) { return x(data.month) - 20 })
        .attr("y", function(data) { return y(data.borrow_count) } )
        .attr("height", function(data) { return graphHeight - y(data.borrow_count) })
        .attr("width", function() { return 20 })
        .attr("fill", "aquamarine")
        .on('mouseover', handleBorrowBarHover)
        .on('mouseout', handleBorrowBarOut)
        .exit();

    //Draw returned bar chart and add event listener
    monthSvg.selectAll('bar.return')
        .data(data)
        .enter()
        .append('rect')
        .attr("x", function(data) { return x(data.month)  })
        .attr("y", function(data) { return y(data.return_count) } )
        .attr("height", function(data) { console.log(data.return_count); return graphHeight - y(data.return_count) })
        .attr("width", function() { return 20 })
        .attr("fill", "blue")
        .on('mouseover', handleReturnBarHover)
        .on('mouseout', handleReturnBarOut)
        .exit();

    //Add annotation for two histogram
    monthSvg.append("circle").attr("cx",450).attr("cy",30).attr("r", 6).style("fill", "aquamarine");
    monthSvg.append("circle").attr("cx",450).attr("cy",60).attr("r", 6).style("fill", "blue");
    monthSvg.append("text").attr("x", 470).attr("y", 30).text("Car borrowed").style("font-size", "15px").attr("alignment-baseline","middle");
    monthSvg.append("text").attr("x", 470).attr("y", 60).text("Car returned").style("font-size", "15px").attr("alignment-baseline","middle");
}


//This function will display the number of borrowed cars when the circle is hover
function handleBorrowLineHover(d, i) {
    let circle = d3.select(this);
    circle
        .style("fill", function() { return 'orange' })
        .attr("r", 10);

    svg.append("text")
        .attr("x", () => { return circle.attr("cx") - 30; })
        .attr("y", function() { return circle.attr("cy") - 25; })
        .attr("id", "b" + d.borrow_count + "-" + i)
        .text(function() {
            return d.borrow_count + " car(s)";  // Value of the text
        });
}


//The same as handleBorrowHover (but for returned cars)
function handleReturnLineHover(d, i) {
    let circle = d3.select(this);
    circle
        .style("fill", function() { return 'orange' })
        .attr("r", 10);

    svg.append("text")
        .attr("x", () => { return circle.attr("cx") - 30; })
        .attr("y", function() { return circle.attr("cy") - 25; })
        .attr("id", "r" + d.return_count + "-" + i)
        .text(function() {
            return d.return_count + " car(s)";  // Value of the text
        });
}


//This function will remove the text created by the handleBorrowLineOver functions
function handleBorrowLineOut(d, i) {
    d3.select(this)
        .style("fill", function() { return 'green' })
        .attr("r", 5);

    svg.select("#b" + d.borrow_count + "-" + i).remove()
}


//The same as handleBorrowLineOut (but for returned cars)
function handleReturnLineOut(d, i) {
    d3.select(this)
        .style("fill", function() { return 'blue' })
        .attr("r", 5);

    svg.select("#r" + d.return_count + "-" + i).remove()
}


//Same as above, but for the bar chart
function handleBorrowBarHover(d, i) {
    bar = d3.select(this)
        .style("fill", function() { return 'yellow' })
        .attr("width", function() { return 22.5 });

    //Add text
    monthSvg.append('text')
        .attr("x", () => { return bar.attr("x") - 20; })
        .attr("y", function() { return bar.attr("y") - 20; })
        .attr("id", "bbar" + d.borrow_count + "-" + i)
        .text(function() {
            return d.borrow_count + " car(s)";  // Value of the text
        });
}

function handleBorrowBarOut(d, i) {
    bar = d3.select(this)
        .style("fill", function() { return 'aquamarine' })
        .attr("width", function() { return 20 });
    monthSvg.select("#bbar" + d.borrow_count + "-" + i).remove()
}

function handleReturnBarHover(d, i) {
    bar = d3.select(this)
        .style("fill", function() { return 'yellow' })
        .attr("width", function() { return 22.5 });

    //Add text
    monthSvg.append('text')
        .attr("x", () => { return bar.attr("x") - 20; })
        .attr("y", function() { return bar.attr("y") - 20; })
        .attr("id", "rbar" + d.return_count + "-" + i)
        .text(function() {
            return d.return_count + " car(s)";  // Value of the text
        });
}

function handleReturnBarOut(d, i) {
    bar = d3.select(this)
        .style("fill", function() { return 'blue' })
        .attr("width", function() { return 20 });
    monthSvg.select("#rbar" + d.return_count + "-" + i).remove()
}
