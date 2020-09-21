import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import api from '../../api';

const Reports = () => {
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

    const columns = [
        {title: "User's Email", field: "email"},
        {title: "Issue", field: "first_name"},
    ];

    return (
        <MaterialTable
            title="List of Issue"
            columns={columns}
            data={data}
        />
    );
}

export default Reports;
