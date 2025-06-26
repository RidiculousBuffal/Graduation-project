import React, { useState, useEffect } from 'react';
import { Select, message } from 'antd';
import { getAllImageInOneFlight } from '@/api/flightapi.ts';
import type { FlightImage } from '@/api/flightapi.ts';

interface AircraftImageSelectorProps {
    flightId?: string;
    value?: string;
    onChange?: (imageId: string, imageInfo: FlightImage) => void;
    placeholder?: string;
    disabled?: boolean;
}

const AircraftImageSelector: React.FC<AircraftImageSelectorProps> = ({
                                                                         flightId,
                                                                         value,
                                                                         onChange,
                                                                         placeholder = "请选择参考底图",
                                                                         disabled = false
                                                                     }) => {
    const [images, setImages] = useState<FlightImage[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (flightId) {
            loadImages();
        } else {
            setImages([]);
        }
    }, [flightId]);

    const loadImages = async () => {
        if (!flightId) return;

        setLoading(true);
        try {
            const result = await getAllImageInOneFlight(flightId);
            if (result) {
                setImages(result);
            }
        } catch (error) {
            console.error('加载飞机图片失败:', error);
            message.error('加载飞机图片失败');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (selectedValue: string) => {
        const selectedImage = images.find(image => image.aircraft_image_id === selectedValue);
        if (selectedImage && onChange) {
            onChange(selectedValue, selectedImage);
        }
    };

    return (
        <Select
            value={value}
            onChange={handleChange}
            placeholder={placeholder}
            disabled={disabled || !flightId}
            loading={loading}
            allowClear
            showSearch
            optionFilterProp="children"
            style={{ width: '100%' }}
        >
            {images.map(image => (
                <Select.Option key={image.aircraft_image_id} value={image.aircraft_image_id}>
                    [{image.image_name}] - {image.aircraft_name}
                </Select.Option>
            ))}
        </Select>
    );
};

export default AircraftImageSelector;