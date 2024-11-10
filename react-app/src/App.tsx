import React, { useEffect, useState } from 'react';
import { Card, Row, Col } from 'antd';
import axios from 'axios';

interface Job {
  title: string;
  abstract: string;
}

const App: React.FC = () => {
  const [data, setData] = useState<Job[]>([]);

  useEffect(() => {
    axios.get('/api/data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  return (
    <div style={{ padding: '30px' }}>
      <Row gutter={16}>
        {data.map((item, index) => (
          <Col span={8} key={index}>
            <Card title={item.title} bordered={false}>
              <p>{item.abstract}</p>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default App;