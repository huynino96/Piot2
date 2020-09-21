import { useState, useEffect } from 'react';
import { Card, CardHeader, CardBody } from 'reactstrap';
import api from '../api';

const Manager = () => {
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

    return (
        <CardBody>
            <CardHeader>
                Data visualization
            </CardHeader>
            <CardBody>
                <h3>Daily Rent/Return plot</h3>
                <div id="graphDailyDiv" className="mb-3" />
                <h3>Monthly Rent/Return histogram</h3>
                <div id="graphMonthlyDiv" />
            </CardBody>
        </CardBody>
    );
};

export default Manager;
