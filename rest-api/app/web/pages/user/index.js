import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import api from '../../api';

const Index = () => {
    const [data, setData] = useState([]);
    const [iserror, setIserror] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        api.get("/users")
            .then(res => {
                setData(res.data.data)
            })
            .catch(error=>{
                setErrorMessage(["Cannot load user data"])
                setIserror(true)
            });
    }, []);

    const handleBook = (event, rowData) => {

    };

    const columns = [
        {title: "id", field: "id", hidden: true},
        {title: "Plate Number", field: "email"},
        {title: "Make", field: "make"},
        {title: "Body Type", field: "body_type"},
        {title: "Color", field: "color"},
        {title: "Seats", field: "seats"},
        {title: "Location", field: "location"},
        {title: "Cost Per Hour", field: "cost_per_hour"},
    ];

    const actions = [
        {
            icon: 'calendar_today',
            tooltip: 'Book',
            onClick: handleBook,
        }
    ];

    return (
        <MaterialTable
            title="Available Car"
            columns={columns}
            data={data}
            actions={actions}
        />
    );
}

export default Index;
