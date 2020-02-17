import React, {useCallback, useState, useEffect} from 'react';
import {useDropzone} from 'react-dropzone';
import Dropzone from 'react-dropzone';
import {uploadFile} from '../../actions.js';
import {
  UploadContainer, CheckBoxContainer, DropArea, PText, PTextLight, ErrorText,
  SuccessText
} from './styles';
import { Tooltip, OverlayTrigger } from 'react-bootstrap';
import { Info } from 'react-feather';

/**
 * Drag n Drop or clickable file upload box
 */
const UploadForm = () => {
  const [notification, setNotification] = useState();
  const [overwrite, setOverwrite] = useState(false);
  let notificationEl;

  if (notification && notification.type && notification.msg) {
    if (notification.type === 'error') {
      notificationEl = <ErrorText>{notification.msg}</ErrorText>
    } else {
      notificationEl = <SuccessText>{notification.msg}</SuccessText>
    }
  }

  // file upload handler
  const onDrop = useCallback(acceptedFiles => {
    setNotification(); // clear notification messages
    let filename = 'File';

    if (acceptedFiles.length > 1) {
      setNotification({
        type: 'error',
        msg: 'Too many files selected. Only single file uploads are supported.'
      });
      return;
    }

    if (acceptedFiles[0].name) {
      filename = acceptedFiles[0].name;
    }

    uploadFile(acceptedFiles, overwrite)
      .then(res => {
        if (res.result === 'UPLOAD_FILE_EXISTS') {
          setNotification({ type: 'error', msg: `${filename} already uploaded. Select the overwrite checkbox to force overwrite any existing data for this scan.` });
        } else if (res.result === 'INVALID_XML') {
          setNotification({ type: 'error', msg: `${filename} is not a valid xml file. Nice try.` });
        } else {
          setNotification({ type: 'success', msg: `${filename} imported successfully.`});
        }
      })
      .catch(e => {
        console.error(e);
        setNotification({ type: 'error', msg: 'Sorry, there was an error importing your file. Please contact support for assistance.'});
      })
  }, [overwrite])

  const {getRootProps, getInputProps, isDragActive} = useDropzone({
    onDrop,
    accept: 'text/xml'
  })

  return (
    <div>
      <UploadContainer>
        <DropArea {...getRootProps()}>
          <input {...getInputProps()} />
          <PText>Import nmap scan results file (.xml)</PText>
          <PTextLight>Drag and drop or click to select file</PTextLight>
        {notificationEl}
        </DropArea>
        <CheckBoxContainer>
          <input type="checkbox" onChange={() => setOverwrite(!overwrite)}/>
          <label><PText>&nbsp; Overwrite &nbsp;</PText></label>
          <OverlayTrigger
            placement='right'
            overlay={
            <Tooltip id='tooltip-right' container="body" >
              Check this option if you are reuploading the same results file (same filename) and
              wish to overwrite/replace its previous scan results.
            </Tooltip>
          }>
            <Info size={17} color="#999999" />
          </OverlayTrigger>
        </CheckBoxContainer>
      </UploadContainer>
    </div>
  )
}

export default UploadForm;
