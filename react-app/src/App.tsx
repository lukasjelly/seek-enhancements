import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Pagination } from 'antd';
import axios from 'axios';
import { Job } from './models/init-models'; // Adjust the import path as necessary

const App: React.FC = () => {
  const [data, setData] = useState<Job[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [pageSize, setPageSize] = useState(10);

  const fetchJobs = (page: number, pageSize: number) => {
    axios.get(`/api/jobs?page=${page}&limit=${pageSize}`)
      .then(response => {
        setData(response.data.data);
        setTotal(response.data.total);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setData([]); // Ensure data is set to an empty array on error
      });
  };

  useEffect(() => {
    fetchJobs(page, pageSize);
  }, [page, pageSize]);

  const handlePageChange = (page: number, pageSize?: number) => {
    setPage(page);
    if (pageSize) {
      setPageSize(pageSize);
    }
  };

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
      <Pagination
        current={page}
        pageSize={pageSize}
        total={total}
        onChange={handlePageChange}
        style={{ marginTop: '20px', textAlign: 'center' }}
      />
    </div>
  );
};

export default App;