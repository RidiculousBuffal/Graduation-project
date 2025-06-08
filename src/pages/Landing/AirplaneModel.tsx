import React, {useRef} from 'react';
import {useFrame} from '@react-three/fiber';
import {useGLTF} from '@react-three/drei';
import {Group} from 'three';

// 使用下载的模型文件
const AirplaneModel: React.FC = () => {
    const groupRef = useRef<Group>(null);

    // 加载 GLTF 模型（将模型文件放在 public/models/ 目录下）
    const {scene} = useGLTF('https://zlcminio.ridiculousbuffal.com/dhu/cute_airplane.glb');

    useFrame((state, delta) => {
        if (groupRef.current) {
            groupRef.current.rotation.y += delta * 0.3;
            groupRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.1;
        }
    });

    return (
        <group ref={groupRef}>
            <primitive
                object={scene}
                scale={[0.01, 0.01, 0.01]} // 调整模型大小
                position={[0, 0, 0]}
            />
        </group>
    );
};

// 预加载模型以提高性能
useGLTF.preload('https://zlcminio.ridiculousbuffal.com/dhu/cute_airplane.glb');

export default AirplaneModel;