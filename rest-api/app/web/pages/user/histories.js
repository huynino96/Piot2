import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import api from '../../api';

const Histories = () => {
    const [data, setData] = useState([]);
    const [iserror, setIserror] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const handleCancel = (event, rowData) => {

    };

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

    const actions = [
        {
            icon: 'close',
            tooltip: 'Cancel',
            onClick: handleCancel,
        }
    ];

    const columns = [
        {title: "Duration", field: "email"},
        {title: "Plate Number", field: "email"},
        {title: "Make", field: "make"},
        {title: "Body Type", field: "body_type"},
        {title: "Color", field: "color"},
        {title: "Seats", field: "seats"},
        {title: "Location", field: "location"},
        {title: "Cost Per Hour", field: "cost_per_hour"},
    ];

    return (
        <MaterialTable
            title="Booked Car"
            columns={columns}
            data={data}
            actions={actions}
        />
    );
};

export default Histories;
