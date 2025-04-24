// src/components/TheaterSeating.tsx
import React, { useRef, useEffect, useState } from 'react';

type SectionLabel = 'Floor1' | 'Floor2' | 'Floor3' | 'Floor4' | 'Floor5' | 'Balcony';

interface Seat {
    id: string; // 新增唯一ID
    x: number;
    y: number;
    color: string;
    column: number;
    row: number;
    section: SectionLabel;
}

interface SectionLayout {
    label: SectionLabel;
    rows: number;
    rowSpacing: number;    // 列间距（水平间距）
    seatSpacing: number;   // 行间距（垂直间距）
    position: string;
    rowColumns?: number[]; // 每行座位数
    maxColumns?: number;   // 最大列数（用于右对齐）
    rotation?: number;     // 旋转角度（度数）
    startX: number;        // 区域起始点X（row1 seat1）
    startY: number;        // 区域起始点Y
    direction?: 'ltr' | 'rtl'; // 排列方向
}

const TheaterSeating = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [seats, setSeats] = useState<Seat[]>([]);
    //const [selectedColor, setSelectedColor] = useState('#ffd700');
    const [hoverSeat, setHoverSeat] = useState<Seat | null>(null);

    const THEATER_LAYOUT = {
        seatSize: 12,
        spacing: 40,
        canvasWidth: 1600,
        canvasHeight: 2000,
        stage: {
            width: 500,
            height: 120,
            x: 550,
            y: 60
        },
        sections: [
            {
                label: 'Floor5',
                rows: 6,
                rowColumns: [3, 5, 7, 9, 11, 12],
                maxColumns: 12,
                rowSpacing: 20,
                seatSpacing: 25,
                position: 'leftleft',
                rotation: 20,    // 向左旋转15度
                direction: 'rtl', // 从右向左排列
                startX: 70,      // 自定义起始点
                startY: 225
            },
            {
                label: 'Floor4',
                rows: 15,
                rowColumns: Array(15).fill(15),
                rowSpacing: 20,
                seatSpacing: 25,
                position: 'left',
                startX: 300,
                startY: 300
            },
            {
                label: 'Floor3',
                rows: 15,
                rowColumns: Array(15).fill(15),
                rowSpacing: 20,
                seatSpacing: 25,
                position: 'center',
                startX: 625,
                startY: 300
            },
            {
                label: 'Floor2',
                rows: 15,
                rowColumns: Array(15).fill(15),
                rowSpacing: 20,
                seatSpacing: 25,
                position: 'right',
                startX: 950,
                startY: 300
            },
            {
                label: 'Floor1',
                rows: 6,
                rowColumns: [3, 5, 7, 9, 11, 12],
                maxColumns: 12,
                rowSpacing: 20,
                seatSpacing: 25,
                position: 'rightright',
                rotation: -20,     // 向右旋转15度
                direction: 'ltr', // 从左向右排列
                startX: 1275,
                startY: 300
            },
            {
                label: 'Balcony',
                rows: 15,
                rowColumns: Array(15).fill(15),
                rowSpacing: 20,
                seatSpacing: 25,
                position: 'rear',
                startX: 625,
                startY: 800
            }
        ] as SectionLayout[]
    };
// 生成旋转后的座位坐标
    const generateRotatedSeats = (layout: SectionLayout) => {
        const seats: Seat[] = [];
        if (!layout.rowColumns || layout.rows !== layout.rowColumns.length) return seats;

        const rotation = layout.rotation || 0;
        const rad = (rotation * Math.PI) / 180;
        const cos = Math.cos(rad);
        const sin = Math.sin(rad);

        for (let row = 0; row < layout.rows; row++) {
            const columns = layout.rowColumns[row];
            const maxColumns = layout.maxColumns || columns;

            // 计算起始位置偏移
            const xOffset = layout.direction === 'rtl'
                ? (maxColumns - columns) * layout.rowSpacing
                : 0;

            for (let col = 0; col < columns; col++) {
                // 计算局部坐标
                let localX = xOffset + col * layout.rowSpacing;
                const localY = row * layout.seatSpacing;

                // 应用旋转
                const rotatedX = layout.startX + localX * cos ;
                const rotatedY = layout.startY + localX * sin + localY * cos;

                // 计算座位号
                const seatNumber = layout.direction === 'rtl'
                    ? columns - col
                    : col + 1;

                seats.push({
                    id: `${layout.label}-R${row + 1}-S${seatNumber}`, // 生成唯一ID
                    x: rotatedX,
                    y: rotatedY,
                    color: 'white',
                    column: seatNumber,
                    row: row + 1,
                    section: layout.label
                });
            }
        }
        return seats;
    };
    // 初始化座位
    useEffect(() => {
        const generateAllSeats = () => {
            return THEATER_LAYOUT.sections.flatMap(section => {
                if (['Floor1', 'Floor5'].includes(section.label)) {
                    return generateRotatedSeats(section);
                }

                // 常规区域生成
                return Array.from({ length: section.rows }, (_, row) =>
                    Array.from({ length: section.rowColumns?.[row] || 15 }, (_, col) => ({
                        id: `${section.label}-R${row + 1}-S${col + 1}`, // 生成唯一ID
                        x: section.startX + col * section.rowSpacing,
                        y: section.startY + row * section.seatSpacing,
                        color: 'white',
                        column: col + 1,
                        row: row + 1,
                        section: section.label
                    }))
                ).flat();
            });
        };

        setSeats(generateAllSeats());
    }, []);

    const drawSectionLabels = (ctx: CanvasRenderingContext2D) => {
        ctx.font = '18px Arial';
        ctx.textBaseline = 'bottom';
        ctx.fillStyle = '#2c3e50';

        THEATER_LAYOUT.sections.forEach(section => {
            const sectionSeats = seats.filter(s => s.section === section.label);
            if (sectionSeats.length === 0) return;

            // 计算标签位置
            const firstSeat = sectionSeats[0];
            const labelX = firstSeat.x;
            const labelY = firstSeat.y - 30;

            ctx.save();
            // 应用旋转
            const rotation = section.rotation || 0;
            ctx.translate(labelX, labelY);
            ctx.rotate((rotation * Math.PI) / 180);
            ctx.fillText(section.label, 0, 0);
            ctx.restore();
        });
    };

    const drawTooltip = (ctx: CanvasRenderingContext2D, seat: Seat) => {
        const text = `ID: ${seat.id}\nSection: ${seat.section}\nRow: ${seat.row}\nSeat: ${seat.column}`;
        const padding = 10;
        const lineHeight = 20;
        const lines = text.split('\n');

        // 计算文本尺寸
        ctx.font = '14px Arial';
        const textMetrics = lines.map(line => ctx.measureText(line));
        const maxWidth = Math.max(...textMetrics.map(m => m.width));
        const textHeight = lines.length * lineHeight;

        // 计算提示框尺寸
        const boxWidth = maxWidth + padding * 2;
        const boxHeight = textHeight + padding * 2;

        // 定位提示框（右侧显示，垂直居中）
        const boxX = seat.x ;
        let boxY = seat.y - boxHeight / 2;

        // 边界检测（防止超出画布底部）
        const canvasBottom = ctx.canvas.height - padding;
        if (boxY + boxHeight > canvasBottom) {
            boxY = canvasBottom - boxHeight;
        }
        // 绘制圆角矩形背景
        ctx.fillStyle = 'rgba(255, 255, 255, 0.97)';
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(boxX, boxY, boxWidth, boxHeight, 6);
        ctx.fill();
        ctx.stroke();

        // 绘制文本（精确对齐）
        ctx.fillStyle = '#222';
        ctx.textBaseline = 'top';
        lines.forEach((line, index) => {
            ctx.fillText(
                line,
                boxX + padding,
                boxY + padding + index * lineHeight
            );
        });
    };


    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawSectionLabels(ctx)
        // 绘制舞台
        ctx.fillStyle = '#e8e8e8';
        ctx.fillRect(
            THEATER_LAYOUT.stage.x,
            THEATER_LAYOUT.stage.y,
            THEATER_LAYOUT.stage.width,
            THEATER_LAYOUT.stage.height
        );
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.strokeRect(
            THEATER_LAYOUT.stage.x,
            THEATER_LAYOUT.stage.y,
            THEATER_LAYOUT.stage.width,
            THEATER_LAYOUT.stage.height
        );

        // 绘制所有座位（带旋转）
        seats.forEach(seat => {
            const sectionLayout = THEATER_LAYOUT.sections.find(s => s.label === seat.section);
            const rotation = sectionLayout?.rotation || 0;
            const rad = (rotation * Math.PI) / 180;

            ctx.save();
            ctx.translate(seat.x, seat.y);
            ctx.rotate(rad);

            const size = THEATER_LAYOUT.seatSize;
            const halfSize = size / 2;

            ctx.fillStyle = seat.color;
            ctx.strokeStyle = '#666';
            ctx.lineWidth = 1;
            ctx.fillRect(-halfSize, -halfSize, size, size);
            ctx.strokeRect(-halfSize, -halfSize, size, size);

            ctx.restore();
        });

        // 绘制悬停提示
        if (hoverSeat) {
            drawTooltip(ctx, hoverSeat);
        }
    }, [seats, hoverSeat]);

    const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        let closestSeat: Seat | null = null;
        const tolerance = THEATER_LAYOUT.seatSize / 2 + 2; // 增加检测容差

        seats.forEach(seat => {
            // 检测鼠标是否在方形区域内
            const inXRange =
                mouseX >= seat.x - tolerance &&
                mouseX <= seat.x + tolerance;
            const inYRange =
                mouseY >= seat.y - tolerance &&
                mouseY <= seat.y + tolerance;

            if (inXRange && inYRange) {
                let minDistance = Infinity;
                // 计算精确距离（可选）
                const dx = seat.x - mouseX;
                const dy = seat.y - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);

                // 只在方形范围内选择最近的座位
                if (!closestSeat || distance < minDistance) {
                    closestSeat = seat;
                    minDistance = distance;
                }
            }
        });

        setHoverSeat(closestSeat);
    };
    //
    // const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    //     if (!hoverSeat) return;
    //
    //     const updatedSeats = seats.map(seat =>
    //         seat === hoverSeat ? { ...seat, color: selectedColor } : seat
    //     );
    //     setSeats(updatedSeats);
    // };

    return (
        <div style={{ padding: '20px' }}>
            <div style={{ marginBottom: 20 }}>
                {/*<label style={{ marginRight: 10 }}>*/}
                {/*    座位颜色选择：*/}
                {/*    <input*/}
                {/*        type="color"*/}
                {/*        value={selectedColor}*/}
                {/*        onChange={(e) => setSelectedColor(e.target.value)}*/}
                {/*    />*/}
                {/*</label>*/}
                {/*<button*/}
                {/*    onClick={() => setSeats(seats.map(s => ({ ...s, color: 'white' })))}*/}
                {/*    style={{ padding: '5px 10px' }}*/}
                {/*>*/}
                {/*    重置所有颜色*/}
                {/*</button>*/}
            </div>
            <canvas
                ref={canvasRef}
                width={THEATER_LAYOUT.canvasWidth}
                height={THEATER_LAYOUT.canvasHeight}
               // onClick={handleCanvasClick}
                onMouseMove={handleMouseMove}
                onMouseLeave={() => setHoverSeat(null)}
                style={{
                    backgroundColor: '#f8f8f8',
                    borderRadius: '8px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                    border: '1px solid #ddd'
                }}
            />
        </div>
    );
};

export default TheaterSeating;