import React from 'react';
import { Form, Button, Container } from 'react-bootstrap';

const FileInput = ({ label, onFileChange }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    onFileChange(file);
  };

  return (
    <Container>
      <Form className="d-flex align-items-center flex-column"> {/* Change to flex-column to align items vertically */}
        <Form.Label style={{ fontWeight: 'bold', fontSize: '1.1em', marginBottom: '5px' }}>{label}</Form.Label> {/* Apply custom styles */}
        <Form.Group controlId="formFile" className="mr-2">
          <Form.Control type="file" onChange={handleFileChange} />
        </Form.Group>
        <Button variant="outline-primary" onClick={() => document.querySelector(`#${label.replace(/\s/g, '')}`).click()}>Upload</Button>
        <input type="file" id={label.replace(/\s/g, '')} style={{ display: 'none' }} onChange={handleFileChange} />
      </Form>
    </Container>
  );
};

export default FileInput;
