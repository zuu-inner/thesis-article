import {
    mkdir,
    readFile,
    writeFile,
} from 'node:fs/promises';

import { dirname } from 'node:path';

export interface ExportOptions {
    svg: string;
    themePath: string;
    outputPath: string;
}

export async function exportSvg(
    options: ExportOptions,
): Promise<void> {
    const css = await readFile(
        options.themePath,
        'utf-8',
    );

    if (!options.svg.includes('<svg')) {
        throw new Error('Invalid SVG document.');
    }

    const style = `<style><![CDATA[
${css}
]]></style>`;

    const svg = options.svg.replace(
        /(<svg\b[^>]*>)/,
        `$1\n${style}`,
    );

    if (svg === options.svg) {
        throw new Error('Unable to inject CSS into SVG.');
    }

    await mkdir(
        dirname(options.outputPath),
        { recursive: true },
    );

    await writeFile(
        options.outputPath,
        svg,
        'utf-8',
    );
}