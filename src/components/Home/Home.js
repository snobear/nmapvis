import React from 'react';
import { useModal, Modal } from 'react-morphing-modal';
import 'react-morphing-modal/dist/ReactMorphingModal.css';
import UploadForm from './../UploadForm/UploadForm';
import { Button, Row, Col, Grid } from 'react-bootstrap';
import { PullRight } from './styles';

/**
 * Home page
 */
const Home = () => {
  const { modalProps, getTriggerProps } = useModal({
    background: '#231C2C',
  });

  return (
    <div>
      <PullRight>
        <Button {...getTriggerProps()}>Upload nmap scan results</Button>
        <Modal {...modalProps}>
          <UploadForm />
        </Modal>
      </PullRight>
    </div>
  )
}

export default Home;
