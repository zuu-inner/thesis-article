import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

import { renderDiagram } from './renderer.js';
import { exportSvg } from './exporter.js';

async function main(): Promise<void> {
    const [inputArg, outputArg, themeArg] =
        process.argv.slice(2);

    if (!inputArg || !outputArg || !themeArg) {
        console.error(
            'Usage: npm run Grapher -- <input.mmd> <output.svg> <theme.css>',
        );

        process.exitCode = 1;
        return;
    }

    const inputPath = resolve(inputArg);
    const outputPath = resolve(outputArg);
    const themePath = resolve(themeArg);

    const source = await readFile(
        inputPath,
        'utf-8',
    );

    const result = renderDiagram(source, {
        fontFamily: 'Arial, Helvetica, sans-serif',
        fontSize: 14,
        padding: 16,
    });

    await exportSvg({
        svg: result.svg,
        themePath,
        outputPath,
    });

    console.log('Export completed.');
    console.log(`Input:  ${inputPath}`);
    console.log(`Output: ${outputPath}`);
    console.log(`Type:   ${result.type}`);
    console.log(`Size:   ${result.width} x ${result.height}`);
}

main().catch((error: unknown) => {
    console.error('Export failed:', error);
    process.exitCode = 1;
});