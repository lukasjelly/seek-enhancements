import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Pagination, Checkbox } from 'antd';
import axios from 'axios';
import { Job } from './models/init-models'; // Adjust the import path as necessary

const App: React.FC = () => {
  const [data, setData] = useState<Job[]>([]);
  const [page, setPage] = useState(1);
  const [totalJobs, setTotal] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [expired, setExpired] = useState(false);

  const fetchJobs = async (page: number, pageSize: number, expired: boolean) => {
    try {
      const response = await axios.get(`/api/jobs?page=${page}&limit=${pageSize}&expired=${expired}`);
      if (Array.isArray(response.data.jobs)) {
        setData(response.data.jobs);
        setTotal(response.data.totalJobs); // Assuming the total is the length of the array
      } else {
        console.error('Unexpected response structure:', response.data);
        setData([]);
        setTotal(0);
      }
    } catch (error) {
      console.error('There was an error fetching the data!', error);
      setData([]); // Ensure data is set to an empty array on error
      setTotal(0);
    }
  };

  useEffect(() => {
    fetchJobs(page, pageSize, expired);
  }, [page, pageSize]);

  const handlePageChange = (page: number, pageSize?: number) => {
    setPage(page);
    if (pageSize) {
      setPageSize(pageSize);
    }
  };

  const handleExpiredChange = (e: any) => {
    setExpired(e.target.checked);
    setPage(1); // Reset page to 1 when changing the expired filter
    fetchJobs(1, pageSize, e.target.checked);
  };

  return (
    <div style={{ padding: '30px' }}>
      <h1>Job Listings</h1>
      <div>
        <Checkbox onChange={handleExpiredChange}>Expired</Checkbox>
      </div>
      <Row gutter={[16, 16]}>
        {data.map((item: Job, index) => {
          return (
            <Col
              key={index}
              xs={24} // 1 column on extra small screens (mobile)
              sm={12} // 2 columns on small screens (tablets)
              md={8} // 3 columns on medium screens (desktops)
              lg={6} // 4 columns on large screens (large desktops)
            >
              <a href={item.shareLink} target="_blank" rel="noopener noreferrer">
                <Card title={item.title} bordered={false}>
                  { <p>{item.abstract}</p> }
                </Card>
              </a>
            </Col>
          );
        })}
      </Row>
      <Pagination
        current={page}
        pageSize={pageSize}
        total={totalJobs}
        onChange={handlePageChange}
        style={{ marginTop: '20px', textAlign: 'center' }}
      />
    </div>
  );
};

export default App;