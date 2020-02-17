import React, {useEffect, useState} from 'react';
import { useModal, Modal } from 'react-morphing-modal';
import 'react-morphing-modal/dist/ReactMorphingModal.css';
import UploadForm from './../UploadForm/UploadForm';
import { Button, Row, Col } from 'react-bootstrap';
import { PullRight, Logo, TopNav, HomeContainer } from './styles';
import ResultsTable from './../ResultsTable/ResultsTable';
import { fetchResults } from '../../actions.js';
import { Shield } from 'react-feather';

/**
 * Home page
 */
const Home = () => {
  const [results, setResults] = useState();

  const { modalProps, getTriggerProps } = useModal({
    background: '#544D5F',
    onClose() {
      // refresh data
      getAllResults();
    },
  });

  const getAllResults = () => {
    fetchResults().then(results => {
      setResults(results);
    })
    .catch(e => {
      console.error(e);
    })
  }

  // side effects to fire on page load
  useEffect(() => {
    getAllResults()
  },[]);

  return (
    <HomeContainer>
      <Row>
        <Shield size={40} color="#C8963E" />
        <Logo>NmapVis</Logo>
      </Row>
      <TopNav>
        <PullRight>
          <Button {...getTriggerProps()}>Upload nmap scan results</Button>
          <Modal {...modalProps}>
            <UploadForm />
          </Modal>
        </PullRight>
      </TopNav>

      <Row>
        <Col>
        { results && results.length > 0 && <ResultsTable data={results}/> }
        { results && results.length == 0 &&
          <PullRight>
            <h3>No scan results. Upload some ^</h3>
          </PullRight>
        }
        </Col>
      </Row>
    </HomeContainer>
  )
}

export default Home;
