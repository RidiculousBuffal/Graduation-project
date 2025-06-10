import React, {useRef, useEffect, useState} from 'react';
import {Button, message} from 'antd';
import {CameraOutlined, ReloadOutlined} from '@ant-design/icons';
import './FaceCapture.css';

interface FaceCaptureProps {
    onCapture: (base64: string) => void;
    width?: number;
    height?: number;
}

const FaceCapture: React.FC<FaceCaptureProps> = ({
                                                     onCapture,
                                                     width = 400,
                                                     height = 300
                                                 }) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const [capturedImage, setCapturedImage] = useState<string>('');

    useEffect(() => {
        startCamera().then(r => r);
        return () => {
            stopCamera();
        };
    }, []);

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {width, height, facingMode: 'user'}
            });

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                setIsStreaming(true);
            }
        } catch (error) {
            message.error('无法访问摄像头，请检查权限设置');
            console.error('Camera access error:', error);
        }
    };

    const stopCamera = () => {
        if (videoRef.current?.srcObject) {
            const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
            tracks.forEach(track => track.stop());
            setIsStreaming(false);
        }
    };

    const capturePhoto = () => {
        if (!videoRef.current || !canvasRef.current) return;

        const canvas = canvasRef.current;
        const video = videoRef.current;
        const ctx = canvas.getContext('2d');

        if (!ctx) return;

        canvas.width = width;
        canvas.height = height;

        ctx.translate(width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0, width, height);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        const base64 = canvas.toDataURL('image/jpeg', 0.8);

        setCapturedImage(base64);
        onCapture(base64);
        message.success('人脸采集成功');
    };

    const retakePhoto = () => {
        setCapturedImage('');
        startCamera().then(r => r);
    };

    return (
        <div className="face-capture-container">
            <div className="camera-preview" style={{width, height}}>
                {!capturedImage ? (
                    <>
                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            muted
                            className="video-stream"
                            style={{width: '100%', height: '100%'}}
                        />
                        <div className="face-guide">
                            <div className="face-outline"></div>

                        </div>
                    </>
                ) : (
                    <img
                        src={capturedImage}
                        alt="Captured face"
                        className="captured-image"
                        style={{width: '100%', height: '100%'}}
                    />
                )}
            </div>

            <canvas ref={canvasRef} style={{display: 'none'}}/>

            <div className="capture-controls">
                {!capturedImage ? (
                    <Button
                        type="primary"
                        size="large"
                        icon={<CameraOutlined/>}
                        onClick={capturePhoto}
                        disabled={!isStreaming}
                        className="capture-btn"
                    >
                        采集人脸
                    </Button>
                ) : (
                    <Button
                        type="default"
                        size="large"
                        icon={<ReloadOutlined/>}
                        onClick={retakePhoto}
                        className="retake-btn"
                    >
                        重新采集
                    </Button>
                )}
            </div>
        </div>
    );
};

export default FaceCapture;