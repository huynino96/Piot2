function getAnalytics() {
    const username = window.localStorage.getItem('username');
    const password = window.localStorage.getItem('password');
    fetch(`http://127.0.0.1:5000/analytics/daily`, {
        method: "GET",
            headers: {
                'Authorization': 'Basic ' + btoa(username + ":" + password)
            }
        })
        .then(resp => resp.json())
        .then(data => drawDailyGraph(data));

    fetch(`http://127.0.0.1:5000/analytics/monthly`, {
        method: "GET",
            headers: {
                'Authorization': 'Basic ' + btoa(username + ":" + password)
            }
        })
        .then(resp => resp.json())
        .then(data => drawMonthlyGraph(data))
}

window.onload = function() {
    if (window.location.pathname.indexOf('manager') > -1) {
        getAnalytics();
    }
};
