import { CardHeader, CardBody } from 'reactstrap';

const Manager = () => {
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
