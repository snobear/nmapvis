import React, {useState} from 'react';
import { TableStyled, ClearBox } from './styles';
import moment from 'moment';
import { Button, Row, Col} from 'react-bootstrap';

/**
 * Table-based listing of results
 */
const ResultsTable = (props) => {
  const [filterIP, setFilterIP] = useState();

  const tableRows = props.data.filter(item => !filterIP || item.addr === filterIP)
    .map(item => {
      return (
        <tr key={item.scan_result_id}>
          <td><a onClick={() => setFilterIP(item.addr)} href="#">{item.addr}</a></td>
          <td>{item.hostname}</td>
          <td>{item.port}</td>
          <td>{item.protocol}</td>
          <td>{item.service_name}</td>
          <td>{item.state}</td>
          <td>{item.reason}</td>
          <td>{ moment.unix(item.start_dt).format('MM/DD/YYYY, h:mm:ss a') }</td>
          <td>{item.filename}</td>
        </tr>
      )
    });

  return (
    <div>
      <h3>nmap Scan Results</h3>
      { !filterIP && <i>Click IP address to filter by IP</i> }
      { filterIP &&
        <ClearBox>
          Showing IP: { filterIP } <Button onClick={() => setFilterIP()}>Clear filter</Button>
        </ClearBox>
      }
      <TableStyled striped bordered hover variant="dark" size="sm">
        <thead>
          <tr>
            <th>IP</th>
            <th>Hostname</th>
            <th>Port</th>
            <th>Protocol</th>
            <th>Service</th>
            <th>Host State</th>
            <th>Reason</th>
            <th>Scan Date</th>
            <th>Source File</th>
          </tr>
        </thead>
        <tbody>
         {tableRows}
        </tbody>
      </TableStyled>
    </div>
  )
}

export default ResultsTable;
