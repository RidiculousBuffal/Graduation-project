import React, {Suspense} from 'react';
import {Layout, Typography, Button, Row, Col, Card, Statistic, Space} from 'antd';
import {
    RocketOutlined,
    SafetyOutlined,
    ThunderboltOutlined,
    EyeOutlined,
    BarChartOutlined,
    ClockCircleOutlined
} from '@ant-design/icons';
import {Canvas} from '@react-three/fiber';
import {OrbitControls, Environment, Float} from '@react-three/drei';
import AirplaneModel from './AirplaneModel';
import './LandingPage.css';

const {Header, Content, Footer} = Layout;
const {Title, Paragraph} = Typography;

const LandingPage: React.FC = () => {
    return (
        <Layout className="landing-page">
            {/* Header */}
            <Header className="header">
                <div className="nav-container">
                    <div className="logo">
                        <RocketOutlined className="logo-icon"/>
                        <span className="logo-text">AeroDetect</span>
                    </div>
                    <Space size="large">
                        <Button type="primary" size="large">开始体验</Button>
                    </Space>
                </div>
            </Header>

            <Content>
                {/* Hero Section */}
                <section className="hero-section">
                    <Row gutter={[48, 48]} align="middle">
                        <Col xs={24} lg={12}>
                            <div className="hero-content">
                                <Title level={1} className="hero-title">
                                    智能大飞机
                                    <br/>
                                    <span className="gradient-text">检测系统</span>
                                </Title>
                                <Paragraph className="hero-description">
                                    基于先进的计算机视觉和深度学习技术，为航空业提供实时、精准的飞机检测与识别解决方案。
                                    提升机场运营效率，保障飞行安全。
                                </Paragraph>
                                <Space size="large" className="hero-buttons">
                                    <Button type="primary" size="large" icon={<EyeOutlined/>}>
                                        立即体验
                                    </Button>
                                    <Button size="large" color={"default"} variant={'dashed'} >
                                        了解更多
                                    </Button>
                                </Space>
                            </div>
                        </Col>
                        <Col xs={24} lg={12}>
                            <div className="hero-3d">
                                <Canvas camera={{position: [0, 0, 5], fov: 75}}>
                                    <Suspense fallback={null}>
                                        <Environment preset="sunset"/>
                                        <ambientLight intensity={0.5}/>
                                        <directionalLight position={[10, 10, 5]} intensity={1}/>
                                        <Float speed={1.5} rotationIntensity={0.5} floatIntensity={0.5}>
                                            <AirplaneModel/>
                                        </Float>
                                        <OrbitControls enableZoom={true} autoRotate autoRotateSpeed={2}/>
                                    </Suspense>
                                </Canvas>
                            </div>
                        </Col>
                    </Row>
                </section>

                {/* Statistics Section */}
                <section className="stats-section">
                    <Row gutter={[32, 32]}>
                        <Col xs={12} sm={6}>
                            <Card className="stat-card">
                                <Statistic
                                    title="检测精度"
                                    value={99.8}
                                    precision={1}
                                    suffix="%"
                                    valueStyle={{color: '#1890ff'}}
                                />
                            </Card>
                        </Col>
                        <Col xs={12} sm={6}>
                            <Card className="stat-card">
                                <Statistic
                                    title="响应时间"
                                    value={50}
                                    suffix="ms"
                                    valueStyle={{color: '#52c41a'}}
                                />
                            </Card>
                        </Col>
                        <Col xs={12} sm={6}>
                            <Card className="stat-card">
                                <Statistic
                                    title="支持机型"
                                    value={200}
                                    suffix="+"
                                    valueStyle={{color: '#722ed1'}}
                                />
                            </Card>
                        </Col>
                        <Col xs={12} sm={6}>
                            <Card className="stat-card">
                                <Statistic
                                    title="服务机场"
                                    value={150}
                                    suffix="+"
                                    valueStyle={{color: '#fa541c'}}
                                />
                            </Card>
                        </Col>
                    </Row>
                </section>

                {/* Features Section */}
                <section className="features-section">
                    <div className="section-header">
                        <Title level={2}>核心特性</Title>
                        <Paragraph>
                            先进的技术架构，为您提供全方位的飞机检测解决方案
                        </Paragraph>
                    </div>
                    <Row gutter={[32, 32]}>
                        <Col xs={24} md={8}>
                            <Card className="feature-card" hoverable>
                                <div className="feature-icon">
                                    <EyeOutlined/>
                                </div>
                                <Title level={4}>实时检测</Title>
                                <Paragraph>
                                    基于深度学习的实时视频流分析，毫秒级响应，准确识别各类大型客机
                                </Paragraph>
                            </Card>
                        </Col>
                        <Col xs={24} md={8}>
                            <Card className="feature-card" hoverable>
                                <div className="feature-icon">
                                    <SafetyOutlined/>
                                </div>
                                <Title level={4}>安全可靠</Title>
                                <Paragraph>
                                    多重安全保障机制，确保系统稳定运行，为机场安全管理提供强力支撑
                                </Paragraph>
                            </Card>
                        </Col>
                        <Col xs={24} md={8}>
                            <Card className="feature-card" hoverable>
                                <div className="feature-icon">
                                    <BarChartOutlined/>
                                </div>
                                <Title level={4}>智能分析</Title>
                                <Paragraph>
                                    提供详细的数据分析报告，帮助优化机场运营流程，提升管理效率
                                </Paragraph>
                            </Card>
                        </Col>
                    </Row>
                </section>

                {/* Technology Section */}
                <section className="tech-section">
                    <Row gutter={[48, 48]} align="middle">
                        <Col xs={24} lg={12}>
                            <div className="tech-3d">
                                <Canvas camera={{position: [0, 0, 8], fov: 60}}>
                                    <Suspense fallback={null}>
                                        <Environment preset="city"/>
                                        <ambientLight intensity={0.6}/>
                                        <pointLight position={[10, 10, 10]}/>
                                        <Float speed={2} rotationIntensity={1} floatIntensity={0.8}>
                                            <mesh>
                                                <boxGeometry args={[2, 2, 2]}/>
                                                <meshStandardMaterial color="#1890ff" wireframe/>
                                            </mesh>
                                        </Float>
                                        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={3}/>
                                    </Suspense>
                                </Canvas>
                            </div>
                        </Col>
                        <Col xs={24} lg={12}>
                            <div className="tech-content">
                                <Title level={2}>先进技术架构</Title>
                                <Space direction="vertical" size="large" className="tech-features">
                                    <div className="tech-item">
                                        <ThunderboltOutlined className="tech-item-icon"/>
                                        <div>
                                            <Title level={5}>深度学习引擎</Title>
                                            <Paragraph>采用最新的 YOLO v8 算法，确保检测精度和速度</Paragraph>
                                        </div>
                                    </div>
                                    <div className="tech-item">
                                        <ClockCircleOutlined className="tech-item-icon"/>
                                        <div>
                                            <Title level={5}>边缘计算</Title>
                                            <Paragraph>本地化部署，降低延迟，提升响应速度</Paragraph>
                                        </div>
                                    </div>
                                    <div className="tech-item">
                                        <BarChartOutlined className="tech-item-icon"/>
                                        <div>
                                            <Title level={5}>云端协同</Title>
                                            <Paragraph>云端数据分析，持续优化模型性能</Paragraph>
                                        </div>
                                    </div>
                                </Space>
                            </div>
                        </Col>
                    </Row>
                </section>


            </Content>

            {/* Footer */}
            <Footer className="footer">
                <div className="footer-content">
                    CopyRight@2025 Licheng Zhou,Donghua University
                </div>
            </Footer>
        </Layout>
    );
};

export default LandingPage;