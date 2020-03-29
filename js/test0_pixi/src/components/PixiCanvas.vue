<template>
    <div id="pixi-canvas-root">
        <div id="canvas"></div>
    </div>
</template>

<script>
    import * as PIXI from 'pixi.js';
    export default {
        name: "PixiCanvas",
        data: function() {
            return {
                canvas: {
                    width: 1100,
                    height: 700,
                    backgroundColor: 0x111111,
                },
                segment: {
                    speed: 0.1,
                    width: 40,
                    height: 170,
                    count: 25,
                    texture_asset: require('@/assets/bulba.png'),
                    position: {
                        x: 60,
                        y: 300
                    }
                },
            }
        },
        computed: {
            app: function(){
                return new PIXI.Application(this.canvas);
            },
        },
        mounted() {
            const app_root = document.getElementById('pixi-canvas-root');
            const app = this.app;
            app_root.innerHTML = '';
            app_root.appendChild(app.view);

            let count = 0;
            const indices = [];
            const coords = [];
            const uvs = [];
            for (let i = 0; i < this.segment.count; i++) {
                coords.push(i * this.segment.width);
                coords.push(this.segment.height * (i % 2));
                uvs.push(i / this.segment.count);
                uvs.push(i % 2);
                indices.push(i);
                indices.push(i + 1);
                indices.push(i + 2);
            }
            indices.pop();
            indices.pop();
            indices.pop();
            indices.pop();

            const segment_texture = PIXI.Texture.from(this.segment.texture_asset);
            const strip = new PIXI.SimpleMesh(segment_texture, coords, uvs,
                new Uint16Array(indices), PIXI.DRAW_MODES.TRIANGLES);

            strip.x = this.segment.position.x;
            strip.y = this.segment.position.y;

            app.stage.addChild(strip);

            app.ticker.add((delta) => {
                count += delta * this.segment.speed;
                for (let i = 0; i < this.segment.count; i++) {
                    coords[ i * 2 ] = i * this.segment.width + Math.cos((i * 0.3) + count) * 20;
                    coords[ i * 2 + 1] = this.segment.height * (i % 2) + Math.sin((i * 0.5) + count) * 30;
                }
            });
        }
    }
</script>

<style scoped>

</style>